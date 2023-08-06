import datetime
import logging
import os
import pathlib
import shutil
import subprocess
import tarfile
from typing import List, Optional, Set, Tuple

import yaml

from mir.commands import base
from mir.tools import checker, data_exporter, hash_utils, mir_storage_ops, revs_parser
from mir.tools.code import MirCode
from ymir_proto.gen import mir_common_pb2 as mir_common
from ymir_proto.gen import mir_entities_pb2 as mirpb
from ymir_proto.util import ids


def _process_model_storage(export_root: str, model_upload_location: str) -> str:
    models = _find_models(os.path.join(export_root, "models"))
    model_paths = models[0]
    model_mAP = models[1]
    if not model_paths:
        raise ValueError("can not find models")
    pack_model_path = os.path.join(export_root, "models.tar.gz")
    _pack_models(model_paths, pack_model_path)
    model_sha1 = hash_utils.sha1sum_for_file(pack_model_path)

    dest_path = os.path.join(model_upload_location, model_sha1)
    _upload_model_pack(pack_model_path, dest_path)
    os.remove(pack_model_path)

    return model_sha1, model_mAP


def _get_class_type_ids(class_types: str) -> Optional[Set[int]]:
    """
    get class type ids of each class names in `class_types`\n
    class id and name mapping is stored in file: type_id_names.csv
    Args:
        class_types: class type names, seperated by ;, for example: person; dog
            empty str means get all types
    Returns:
        None: all types
        empty set: all class type names are not found, or nothing found in type_id_names.csv
        normal set: ids for each type, order of ids is not the same as type names in arg
    """
    if not class_types:
        return None

    cls_mgr = ids.ClassIdManager()
    return set(cls_mgr.id_for_names(class_types.split(";")))


def _find_models(model_root: str) -> Tuple[List[str], float]:
    """
    find models in `model_root`, and returns model names and mAP

    Args:
        model_root (str): model root

    Returns:
        Tuple[List[str], float]: list of model names and map
    """
    model_names = []
    model_mAP = 0

    with open(os.path.join(model_root, "result.yaml"), "r") as f:
        yaml_obj = yaml.safe_load(f.read())
        model_names = yaml_obj["model"]
        model_mAP = float(yaml_obj["map"])

    return ([os.path.join(model_root, name) for name in model_names], model_mAP)


def _pack_models(model_paths: List[str], dest_path: str) -> bool:
    if not model_paths or not dest_path:
        raise ValueError("invalid model_paths or dest_path")

    with tarfile.open(dest_path, "w:gz") as dest_tar_gz:
        for model_path in model_paths:
            logging.info("added {} as {}".format(model_path, os.path.basename(model_path)))
            dest_tar_gz.add(model_path, os.path.basename(model_path))
    return True


def _upload_model_pack(model_pack_path: str, dest_path: str) -> bool:
    # TODO: UPLOAD TO MODEL SERVER WHEN WE HAVE
    if not model_pack_path or not dest_path:
        raise ValueError("invalid model_pack_path or dest_path")

    shutil.copyfile(model_pack_path, dest_path)
    return True


def _update_mir_tasks(mir_root: str, base_branch: str, dst_branch: str, task_id: str, model_sha1: str, mAP: float):
    """
    add a new mir single task into mir_tasks from branch base_task_id, and save it to a new branch: task_id
    """
    task = mirpb.Task()
    task.type = mir_common.TaskTypeTraining
    task.name = "training done"
    task.task_id = task_id
    task.timestamp = int(datetime.datetime.now().timestamp())
    task.model.model_hash = model_sha1
    task.model.mean_average_precision = mAP

    mir_tasks = mir_storage_ops.MirStorageOps.load_single(mir_root=mir_root,
                                                          mir_branch=base_branch,
                                                          ms=mir_common.MirStorage.MIR_TASKS)
    mir_storage_ops.add_mir_task(mir_tasks, task)
    mir_storage_ops.MirStorageOps.save_and_commit(mir_root=mir_root,
                                                  mir_branch=dst_branch,
                                                  his_branch=base_branch,
                                                  mir_datas={mir_common.MirStorage.MIR_TASKS: mir_tasks},
                                                  commit_message=task_id)

    logging.info("task id: {}, model hash: {}, mAP: {}".format(task_id, model_sha1, mAP))


# add this function for mock unit test.
def _run_train_cmd(cmd: str):
    logging.info("training with cmd: {}".format(cmd))
    run_result = subprocess.run(cmd.split(" "))  # run and wait

    # when train process done
    if run_result.returncode != 0:
        logging.error("training error occured: {}".format(run_result.returncode))
        return MirCode.RC_ERROR_UNKNOWN

    return MirCode.RC_OK


def _generate_config(out_config_path: str, task_id: str, gpus: str, class_names: List[str]):
    with open(str(pathlib.Path(__file__).parent.parent.joinpath("conf/training-template.yaml")), "r") as f:
        config = yaml.safe_load(f)

    config["task_id"] = task_id
    config["gpu_train"] = gpus or ""
    config["class_names"] = class_names
    config["class_num"] = len(class_names)
    # config['epochs'] = 20  # ! for test

    with open(out_config_path, "w") as f:
        yaml.dump(config, f)


class CmdTrain(base.BaseCommand):
    def run(self):
        logging.debug("command train: %s", self.args)

        return CmdTrain.run_with_args(type_names=self.args.predicates,
                                      export_root=self.args.work_dir,
                                      model_upload_location=self.args.model_path,
                                      src_revs=self.args.src_revs,
                                      dst_rev=self.args.dst_rev,
                                      mir_root=self.args.mir_root,
                                      gpu=self.args.gpu,
                                      media_location=self.args.media_location,
                                      executor=self.args.executor)

    @staticmethod
    def run_with_args(type_names: str,
                      export_root: str,
                      model_upload_location: str,
                      executor: str,
                      src_revs: str,
                      dst_rev: str,
                      mir_root: str = None,
                      media_location: str = None,
                      gpu: str = None) -> int:
        if not model_upload_location:
            logging.error("invalid model upload location; abort")
            return MirCode.RC_ERROR_INVALID_ARGS
        src_typ_rev_tid = revs_parser.parse_single_arg_rev(src_revs)
        if not src_revs or not src_typ_rev_tid.rev:
            logging.error("invalid --src-revs; abort")
            return MirCode.RC_ERROR_INVALID_ARGS
        dst_typ_rev_tid = revs_parser.parse_single_arg_rev(dst_rev)
        if not dst_rev or not dst_typ_rev_tid.rev or not dst_typ_rev_tid.tid:
            logging.error("invalid --dst-rev; abort")
            return MirCode.RC_ERROR_INVALID_ARGS
        if not export_root:
            logging.error("empty export_root: abort")
            return MirCode.RC_ERROR_INVALID_ARGS

        if not mir_root:
            mir_root = "."

        return_code = checker.check(mir_root)
        if return_code != MirCode.RC_OK:
            return return_code

        task_id = dst_typ_rev_tid.tid
        base_task_id = src_typ_rev_tid.tid
        if not base_task_id:
            mir_tasks = mir_storage_ops.MirStorageOps.load_single(mir_root=mir_root,
                                                                  mir_branch=src_typ_rev_tid.rev,
                                                                  ms=mir_common.MirStorage.MIR_TASKS)
            base_task_id = mir_tasks.head_task_id
        if not base_task_id:
            logging.error("can not find base task id from both --dst-rev or head task id")
            return MirCode.RC_ERROR_INVALID_ARGS

        # get train_ids, val_ids, test_ids
        train_ids = set()  # type: Set[str]
        val_ids = set()  # type: Set[str]
        test_ids = set()  # type: Set[str]
        unused_ids = set()  # type: Set[str]
        mir_datas = mir_storage_ops.MirStorageOps.load(mir_root=mir_root,
                                                       mir_branch=src_typ_rev_tid.rev,
                                                       mir_storages=[mir_common.MirStorage.MIR_METADATAS])
        mir_metadatas = mir_datas[mir_common.MirStorage.MIR_METADATAS]
        for asset_id, asset_attr in mir_metadatas.attributes.items():
            if asset_attr.tvt_type == mir_common.TvtTypeTraining:
                train_ids.add(asset_id)
            elif asset_attr.tvt_type == mir_common.TvtTypeValidation:
                val_ids.add(asset_id)
            elif asset_attr.tvt_type == mir_common.TvtTypeTest:
                test_ids.add(asset_id)
            else:
                unused_ids.add(asset_id)
        if not train_ids:
            logging.error("no training set; abort")
            return MirCode.RC_ERROR_INVALID_ARGS
        if not val_ids:
            logging.error("no validation set; abort")
            return MirCode.RC_ERROR_INVALID_ARGS

        if not unused_ids:
            logging.info(f"training: {len(train_ids)}, validation: {len(val_ids)}, test: {len(test_ids)}")
        else:
            logging.warning(f"training: {len(train_ids)}, validation: {len(val_ids)}, test: {len(test_ids)}, "
                            f"unused: {len(unused_ids)}")

        # export
        logging.info("exporting assets")
        os.makedirs(export_root, exist_ok=True)
        work_dir_in = os.path.join(export_root, "in")
        work_dir_out = os.path.join(export_root, "out")
        os.makedirs(work_dir_in, exist_ok=True)
        os.makedirs(work_dir_out, exist_ok=True)

        type_ids_set = _get_class_type_ids(type_names)
        if not type_ids_set:
            logging.info("type ids empty, please check -p args")
            return MirCode.RC_ERROR_INVALID_ARGS

        # export train set
        work_dir_in_train = os.path.join(work_dir_in, 'train')
        if os.path.isdir(work_dir_in_train):
            shutil.rmtree(work_dir_in_train)
        data_exporter.export(mir_root=mir_root,
                             assets_location=media_location,
                             class_type_ids=type_ids_set,
                             asset_ids=train_ids,
                             asset_dir=work_dir_in_train,
                             annotation_dir=work_dir_in_train,
                             need_suffix=True,
                             base_branch=src_typ_rev_tid.rev,
                             format_type=data_exporter.ExportFormat.EXPORT_FORMAT_ARK)
        data_exporter.generate_asset_index_file(asset_dir=work_dir_in_train,
                                                rel_start_dir=work_dir_in_train,
                                                index_file_path=os.path.join(work_dir_in_train, 'index.tsv'))

        # export validation set
        work_dir_in_val = os.path.join(work_dir_in, 'val')
        if os.path.isdir(work_dir_in_val):
            shutil.rmtree(work_dir_in_val)
        data_exporter.export(mir_root=mir_root,
                             assets_location=media_location,
                             class_type_ids=type_ids_set,
                             asset_ids=val_ids,
                             asset_dir=work_dir_in_val,
                             annotation_dir=work_dir_in_val,
                             need_suffix=True,
                             base_branch=src_typ_rev_tid.rev,
                             format_type=data_exporter.ExportFormat.EXPORT_FORMAT_ARK)
        data_exporter.generate_asset_index_file(asset_dir=work_dir_in_val,
                                                rel_start_dir=work_dir_in_val,
                                                index_file_path=os.path.join(work_dir_in_val, 'index.tsv'))

        # export test set (if we have)
        if test_ids:
            work_dir_in_test = os.path.join(work_dir_in, 'test')
            if os.path.isdir(work_dir_in_test):
                shutil.rmtree(work_dir_in_test)
            data_exporter.export(mir_root=mir_root,
                                 assets_location=media_location,
                                 class_type_ids=type_ids_set,
                                 asset_ids=test_ids,
                                 asset_dir=work_dir_in_test,
                                 annotation_dir=work_dir_in_test,
                                 need_suffix=True,
                                 base_branch=src_typ_rev_tid.rev,
                                 format_type=data_exporter.ExportFormat.EXPORT_FORMAT_ARK)
            data_exporter.generate_asset_index_file(asset_dir=work_dir_in_test,
                                                    rel_start_dir=work_dir_in_test,
                                                    index_file_path=os.path.join(work_dir_in_test, 'index.tsv'))

        logging.info("starting train docker container")

        # generate configs
        _generate_config(out_config_path=os.path.join(work_dir_in, "config.yaml"),
                         task_id=task_id,
                         gpus=gpu,
                         class_names=ids.ClassIdManager().all_main_names())

        # start train docker and wait
        path_binds = []
        path_binds.append(f"-v {work_dir_in}:/in")
        path_binds.append(f"-v {work_dir_out}:/out")
        joint_path_binds = " ".join(path_binds)
        cmd = (f"nvidia-docker run -it --rm --shm-size=128G {joint_path_binds} --user {os.getuid()}:{os.getgid()} "
               f"{executor}")  # mir-train-gpu:0.1.1.210824

        ret = _run_train_cmd(cmd)
        if ret != MirCode.RC_OK:
            return ret

        # save model
        logging.info("saving models")
        model_sha1, model_mAP = _process_model_storage(work_dir_out, model_upload_location)
        # update metadatas and task with finish state and model hash
        logging.info("creating task")
        _update_mir_tasks(mir_root=mir_root,
                          base_branch=base_task_id,
                          dst_branch=dst_typ_rev_tid.rev,
                          task_id=task_id,
                          model_sha1=model_sha1,
                          mAP=model_mAP)

        logging.info("training done")

        return MirCode.RC_OK


def bind_to_subparsers(subparsers, parent_parser):  # pragma: no cover
    train_arg_parser = subparsers.add_parser("train",
                                             parents=[parent_parser],
                                             description="use this command to train current workspace",
                                             help="train current workspace")
    train_arg_parser.add_argument("-p",
                                  required=True,
                                  dest="predicates",
                                  type=str,
                                  help="predicates to annotations, separated by ;")
    train_arg_parser.add_argument("--model-location",
                                  required=True,
                                  dest="model_path",
                                  type=str,
                                  help="storage place (upload location) to store packed model")
    train_arg_parser.add_argument("--media-location",
                                  required=True,
                                  dest="media_location",
                                  type=str,
                                  help="media storage location for models")
    train_arg_parser.add_argument("--gpu",
                                  dest="gpu",
                                  type=str,
                                  help="gpu ids for training, sep by commas, if not set, uses cpu")
    train_arg_parser.add_argument("-w", required=True, dest="work_dir", type=str, help="work place for training")
    train_arg_parser.add_argument("--executor",
                                  required=True,
                                  dest="executor",
                                  type=str,
                                  help="docker image name for training")
    train_arg_parser.add_argument("--src-revs", dest="src_revs", type=str, help="rev@bid: source rev and base task id")
    train_arg_parser.add_argument("--dst-rev",
                                  dest="dst_rev",
                                  type=str,
                                  required=True,
                                  help="rev@tid: destination branch name and task id")
    train_arg_parser.set_defaults(func=CmdTrain)
