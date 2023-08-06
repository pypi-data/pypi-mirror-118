import logging
import os
import pathlib
import shutil
import subprocess
import tarfile
from typing import List
import time
import yaml

from mir.commands import base
from mir.tools import checker, code, data_exporter, mir_storage, mir_storage_ops, revs_parser
from mir.tools import utils as mir_utils
from ymir_proto.gen import mir_common_pb2 as mir_common
from ymir_proto.gen import mir_entities_pb2 as mirpb


class CmdMining(base.BaseCommand):
    def run(self):
        logging.debug("command mine: %s", self.args)

        return CmdMining.run_with_args(export_root=self.args.work_dir,
                                       src_revs=self.args.src_revs,
                                       dst_rev=self.args.dst_rev,
                                       mir_root=self.args.mir_root,
                                       model_hash=self.args.model_hash,
                                       model_location=self.args.model_location,
                                       media_location=self.args.media_location,
                                       topk=self.args.topk)

    @staticmethod
    def run_with_args(export_root, src_revs, dst_rev, mir_root, model_hash, media_location, model_location, topk=0):
        """
        runs a mining task \n
        Args:
            export_root: mining docker container's work directory
            src_revs: data branch name and base task id
            dst_rev: destination branch name and task id
            mir_root: mir repo path, in order to run in non-mir folder.
            model_hash: used to target model, use prep_tid if non-set
            media_location, model_location: location of assets.
        Returns:
            error code
        """
        # Step 1: check and prepare environment.
        if not mir_root:
            mir_root = '.'
        if not export_root:
            logging.error("empty export_root: abort")
            return code.MirCode.RC_ERROR_INVALID_ARGS
        if not media_location or not model_location:
            logging.error("media or model location cannot be none!")
            return code.MirCode.RC_ERROR_INVALID_ARGS
        if not model_hash:
            logging.error("model_hash is required.")
            return code.MirCode.RC_ERROR_INVALID_ARGS

        if not src_revs or not dst_rev:
            logging.error("invalid --src-revs or --dst-rev; abort")
            return code.MirCode.RC_ERROR_INVALID_ARGS
        src_typ_rev_tid = revs_parser.parse_single_arg_rev(src_revs)
        if not src_typ_rev_tid.rev:
            logging.error(f"no rev found in --src-revs: {src_revs}")
            return code.MirCode.RC_ERROR_INVALID_ARGS
        dst_typ_rev_tid = revs_parser.parse_single_arg_rev(dst_rev)
        if not dst_typ_rev_tid.rev or not dst_typ_rev_tid.tid:
            logging.error(f"no rev or tid found in --dst-rev: {dst_rev}")
            return code.MirCode.RC_ERROR_INVALID_ARGS

        return_code = checker.check(mir_root)
        if return_code != code.MirCode.RC_OK:
            return return_code

        export_in = os.path.join(export_root, "in")  # docker container's input data directory
        export_out = os.path.join(export_root, "out")  # docker container's output data directory
        ret = _prepare_env(export_root=export_root, export_in=export_in, export_out=export_out)
        if ret != code.MirCode.RC_OK:
            logging.error("envron error!")
            return ret

        # Step 3: place data in required format and location.
        _parepare_mining_data(mir_root=mir_root,
                              base_branch=src_typ_rev_tid.rev,
                              input_path=export_in,
                              model_hash=model_hash,
                              model_location=model_location,
                              media_location=media_location,
                              task_id=dst_typ_rev_tid.tid)

        # Step 4: Mining job, start mining docker and wait.
        _run_docker_command(v_in=export_in, v_out=export_out, docker_image='al:0.0.1.b')

        # Step 4: Update mir commits.
        _process_mining_results(mir_root=mir_root,
                                export_out=export_out,
                                dst_typ_rev_tid=dst_typ_rev_tid,
                                src_typ_rev_tid=src_typ_rev_tid,
                                model_hash=model_hash,
                                topk=topk)
        logging.info("mining done, results at: %s", export_out)

        return code.MirCode.RC_OK


def _process_mining_results(mir_root: str, export_out: str, dst_typ_rev_tid: revs_parser.TypRevTid,
                            src_typ_rev_tid: revs_parser.TypRevTid, model_hash: str, topk: int):
    # step 1: build topk results:
    if topk < 0:
        raise RuntimeError("topk cannot be negative")
    topk_result_tsv = os.path.join(export_out, 'result.tsv')
    if not os.path.isfile(topk_result_tsv):
        raise RuntimeError("Cannot find result file {}".format(topk_result_tsv))
    idx_cnt, ret_asset_set = 0, set()
    with open(topk_result_tsv) as ret_f:
        for line in ret_f:
            line = line.strip()
            if not line:
                continue
            if topk > 0 and idx_cnt >= topk:
                break
            ret_asset_set.add(os.path.basename(line.split('\t')[0]))
            idx_cnt += 1
    logging.info("top {} samples found".format(len(ret_asset_set)))

    # step 2: update mir data files
    mir_datas = mir_storage_ops.MirStorageOps.load(mir_root=mir_root,
                                                   mir_branch=src_typ_rev_tid.rev,
                                                   mir_storages=mir_storage.get_all_mir_storage())
    mir_metadatas = mir_datas[mir_common.MirStorage.MIR_METADATAS]
    mir_annotations = mir_datas[mir_common.MirStorage.MIR_ANNOTATIONS]
    mir_keywords = mir_datas[mir_common.MirStorage.MIR_KEYWORDS]
    mir_tasks = mir_datas[mir_common.MirStorage.MIR_TASKS]

    # update mir metadatas
    matched_mir_metadatas = mirpb.MirMetadatas()
    for asset_id in ret_asset_set:
        matched_mir_metadatas.attributes[asset_id].CopyFrom(mir_metadatas.attributes[asset_id])
    logging.info("matched: %d, overriding metadatas.mir", len(matched_mir_metadatas.attributes))

    # update mir annotations
    task_annotation = mir_annotations.task_annotations[mir_annotations.head_task_id]
    joint_asset_ids_set = set(task_annotation.image_annotations.keys()) & ret_asset_set
    matched_mir_annotations = mirpb.MirAnnotations()
    matched_task_annotation = matched_mir_annotations.task_annotations[dst_typ_rev_tid.tid]
    for asset_id in joint_asset_ids_set:
        matched_task_annotation.image_annotations[asset_id].CopyFrom(task_annotation.image_annotations[asset_id])

    # update mir keywords
    joint_asset_ids_set = set(mir_keywords.keywords.keys()) & ret_asset_set
    matched_mir_keywords = mirpb.MirKeywords()
    for asset_id in joint_asset_ids_set:
        matched_mir_keywords.keywords[asset_id].CopyFrom(mir_keywords.keywords[asset_id])

    # update_mir_task
    task = mirpb.Task()
    task.type = mir_common.TaskTypeMining
    task.name = "mining"
    task.task_id = dst_typ_rev_tid.tid
    task.timestamp = int(time.time())
    task.model.model_hash = model_hash
    mir_storage_ops.add_mir_task(mir_tasks, task)

    # step 3: store results and commit.
    # TODO: add inference results into annotations.
    mir_datas = {
        mir_common.MirStorage.MIR_METADATAS: matched_mir_metadatas,
        mir_common.MirStorage.MIR_ANNOTATIONS: matched_mir_annotations,
        mir_common.MirStorage.MIR_KEYWORDS: matched_mir_keywords,
        mir_common.MirStorage.MIR_TASKS: mir_tasks,
    }
    mir_storage_ops.MirStorageOps.save_and_commit(mir_root=mir_root,
                                                  his_branch=src_typ_rev_tid.rev,
                                                  mir_branch=dst_typ_rev_tid.rev,
                                                  mir_datas=mir_datas,
                                                  commit_message=dst_typ_rev_tid.tid)

    return code.MirCode.RC_OK


def _get_model_hash(mir_root: str, prep_tid: str):
    # read `mir_task: mirpb.Task` from current tasks.mir (with `prep_tid`)
    mir_pre_task = mirpb.MirTasks()
    mir_tasks_path = os.path.join(mir_root, "tasks.mir")
    if not os.path.isfile(mir_tasks_path):
        raise ValueError("tasks.mir not found")
    with open(mir_tasks_path, "rb") as f:
        mir_pre_task.ParseFromString(f.read())
    if prep_tid not in mir_pre_task.tasks.keys():
        raise ValueError("cannot find prep task id: {} in tasks.mir".format(prep_tid))
    model_hash = mir_pre_task.tasks[prep_tid].model_hash
    if not model_hash:
        raise ValueError("empty model hash for task: {}".format(prep_tid))
    return model_hash


def _prepare_env(export_root: str, export_in: str, export_out: str):
    if os.path.exists(export_root):
        shutil.rmtree(export_root)
    os.makedirs(export_root, exist_ok=True)
    os.makedirs(export_in, exist_ok=True)
    os.makedirs(export_out, exist_ok=True)

    return code.MirCode.RC_OK


def _run_docker_command(v_in: str, v_out: str, docker_image: str):
    if not os.path.isdir(v_in) or not os.path.isdir(v_out) or not docker_image:
        raise ValueError("run_docker_command: Invalid input args.")

    bind_path = "-v {}:/in -v {}:/out".format(v_in, v_out)
    cmd = "docker run -it --rm {} --user {}:{} {}".format(bind_path, os.getuid(), os.getgid(), docker_image)
    logging.info("starting mining docker container with cmd %s", cmd)
    run_result = subprocess.run(cmd.split(" "), check=True)  # run and wait

    # when mining process done
    if run_result.returncode != 0:
        logging.info("mining error occured: %s", run_result.returncode)
        return code.MirCode.RC_ERROR_UNKNOWN

    return run_result


def _unpack_models(tar_file: str, dest_root: str, sub_folder: str) -> list:
    if not os.path.isdir(dest_root) or not os.path.isfile(tar_file):
        raise ValueError("_unpack_models args error")
    dest_path = os.path.join(dest_root, sub_folder)
    os.makedirs(dest_path, exist_ok=True)

    params_file, json_file = None, None
    with tarfile.open(tar_file, 'r') as tar_gz:
        for item in tar_gz:
            logging.info("extracting %s, %s", item, dest_path)
            if 'json' in item.name:
                json_file = item.name
            if 'params' in item.name:
                params_file = item.name
            tar_gz.extract(item, dest_path)
    return [os.path.join(sub_folder, i) for i in [params_file, json_file]]


def _parepare_mining_data(mir_root: str, base_branch: str, input_path: str, model_hash: str, model_location: str,
                          media_location: str, task_id: str) -> None:

    # Step 1: prepare images.
    _place_media(mir_root=mir_root, base_branch=base_branch, input_path=input_path, media_location=media_location)

    # Step 2: place pretrained model.
    logging.info("fetching model hash {}".format(model_hash))
    [in_container_model_params_path, _] = _place_model(model_hash=model_hash,
                                                       root_path=input_path,
                                                       sub_folder='model',
                                                       model_location=model_location)

    # Step 3: update yaml config file.
    with open(str(pathlib.Path(__file__).parent.parent / "conf/mining-template.yaml")) as f:
        config = yaml.safe_load(f)
    config["model_params_path"] = os.path.join('/in', in_container_model_params_path)
    config["task_id"] = task_id
    logging.debug("config: {}".format(config))
    with open(os.path.join(input_path, 'config.yaml'), 'w') as f:
        yaml.dump(config, f)

    return code.MirCode.RC_OK


def _place_media(mir_root: str, base_branch: str, input_path: str, media_location: str):
    metadata = mir_storage_ops.MirStorageOps.load_single(mir_root=mir_root,
                                                         mir_branch=base_branch,
                                                         ms=mir_common.MirStorage.MIR_METADATAS)
    if len(metadata.attributes) == 0:
        raise ValueError("no assets found in metadatas.mir")

    candidate_path = os.path.join(input_path, 'candidate')
    os.makedirs(candidate_path, exist_ok=True)

    img_list = list(metadata.attributes.keys())  # type: List[str]
    data_exporter.export(mir_root=mir_root,
                         assets_location=media_location,
                         class_type_ids={},
                         asset_ids=img_list,
                         asset_dir=candidate_path,
                         annotation_dir=None,
                         need_suffix=True,
                         base_branch=base_branch,
                         format_type=data_exporter.ExportFormat.EXPORT_FORMAT_NO_ANNOTATION)
    data_exporter.generate_asset_index_file(asset_dir=candidate_path,
                                            rel_start_dir=candidate_path,
                                            index_file_path=os.path.join(candidate_path, 'index.tsv'))


def _place_model(model_hash: str, root_path: str, sub_folder: str, model_location: str):
    """
    place model (named by model_hash) from root_path to model_folder, under sub_folder folder.
    """
    model_id_rel_paths = mir_utils.store_assets_to_dir(asset_ids=[model_hash],
                                                       out_root=root_path,
                                                       sub_folder=sub_folder,
                                                       asset_location=model_location,
                                                       need_suffix=False)
    model_path_abs = os.path.join(root_path, model_id_rel_paths[model_hash])
    ret = _unpack_models(tar_file=model_path_abs, dest_root=root_path, sub_folder=sub_folder)
    return ret


def bind_to_subparsers(subparsers, parent_parser):  # pragma: no cover
    mining_arg_parser = subparsers.add_parser("mining",
                                              parents=[parent_parser],
                                              description="use this command to mine in current workspace",
                                              help="mine current workspace")
    mining_arg_parser.add_argument("-w",
                                   required=True,
                                   dest="work_dir",
                                   type=str,
                                   help="work place for mining and monitoring")
    mining_arg_parser.add_argument("--model-location",
                                   required=True,
                                   dest="model_location",
                                   type=str,
                                   help="model storage location for models")
    mining_arg_parser.add_argument("--media-location",
                                   required=True,
                                   dest="media_location",
                                   type=str,
                                   help="media storage location for models")
    mining_arg_parser.add_argument("--topk",
                                   dest="topk",
                                   type=int,
                                   default=0,
                                   help="If set, discard samples out of topk, sorting by scores.")
    mining_arg_parser.add_argument("--model-hash",
                                   dest="model_hash",
                                   type=str,
                                   required=True,
                                   help="model hash to be used")
    mining_arg_parser.add_argument("--src-revs",
                                   dest="src_revs",
                                   type=str,
                                   required=True,
                                   help="rev@bid: source rev and base task id")
    mining_arg_parser.add_argument("--dst-rev",
                                   dest="dst_rev",
                                   type=str,
                                   required=True,
                                   help="rev@tid: destination branch name and task id")
    mining_arg_parser.set_defaults(func=CmdMining)
