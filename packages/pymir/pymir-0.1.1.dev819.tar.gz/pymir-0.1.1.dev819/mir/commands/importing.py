import datetime
import logging
import os
import shutil

from mir.commands import base
from mir.tools import annotations, code, hash_utils, metadatas, mir_storage_ops, revs_parser
from ymir_proto.gen import mir_common_pb2 as mir_common
from ymir_proto.gen import mir_entities_pb2 as mirpb


class CmdImport(base.BaseCommand):
    def run(self):
        logging.debug("command import: %s", self.args)

        return CmdImport.run_with_args(mir_root=self.args.mir_root,
                                       index_abs=self.args.index_file,
                                       anno_abs=self.args.anno,
                                       gen_abs=self.args.gen,
                                       dataset_name=self.args.dataset_name,
                                       dst_rev=self.args.dst_rev,
                                       src_revs=self.args.src_revs)

    @staticmethod
    def run_with_args(mir_root: str, index_abs: str, anno_abs: str, gen_abs: str, dataset_name: str, dst_rev: str,
                      src_revs: str):
        # Step 1: check args and prepare environment.
        if not index_abs or not anno_abs or not gen_abs:
            logging.error("Missing input args")
            return code.MirCode.RC_ERROR_INVALID_ARGS
        if not os.path.isdir(anno_abs) or not os.path.isfile(index_abs):
            logging.error("Incorrect input paths")
            return code.MirCode.RC_ERROR_INVALID_ARGS
        if not dst_rev:
            logging.error("empty --dst-rev")
            return code.MirCode.RC_ERROR_INVALID_ARGS
        dst_typ_rev_tid = revs_parser.parse_single_arg_rev(dst_rev)
        if not dst_typ_rev_tid.rev or not dst_typ_rev_tid.tid:
            logging.error(f"destination branch or task id not provided: {dst_rev}")
            return code.MirCode.RC_ERROR_INVALID_ARGS
        if not dataset_name:
            dataset_name = dst_typ_rev_tid.tid

        # Step 2: generate sha1 file and rename images.
        # sha1 file to be written.
        sha1_index_abs = os.path.join(gen_abs, os.path.basename(index_abs) + '.sha1')
        sha1_folder_abs = os.path.join(gen_abs, 'hashed')
        ret = _generate_sha_and_cp(index_abs, sha1_index_abs, sha1_folder_abs)
        if ret != code.MirCode.RC_OK:
            logging.error("importing sha1 error.")
            return ret

        # Step 3 import metadat and annotations:
        mir_metadatas = mirpb.MirMetadatas()
        ret = metadatas.import_metadatas(mir_metadatas=mir_metadatas,
                                         dataset_name=dataset_name,
                                         in_sha1_path=sha1_index_abs,
                                         hashed_asset_root=sha1_folder_abs)
        if ret != code.MirCode.RC_OK:
            logging.error("importing metadatas error.")
            return ret

        mir_annotation = mirpb.MirAnnotations()
        mir_keywords = mirpb.MirKeywords()
        ret = annotations.import_annotations(mir_annotation=mir_annotation,
                                             mir_keywords=mir_keywords,
                                             in_sha1_file=sha1_index_abs,
                                             annotations_dir_path=anno_abs,
                                             task_id=dst_typ_rev_tid.tid)
        if ret != code.MirCode.RC_OK:
            logging.error("importing annotations error.")
            return ret

        # create and write tasks
        mir_tasks = mirpb.MirTasks()
        task = mirpb.Task()
        task.type = mir_common.TaskTypeImportData
        task.name = f"importing {index_abs}-{anno_abs}-{gen_abs} as {dataset_name}"
        task.task_id = dst_typ_rev_tid.tid
        task.timestamp = int(datetime.datetime.now().timestamp())
        mir_storage_ops.add_mir_task(mir_tasks, task)

        mir_data = {
            mir_common.MirStorage.MIR_METADATAS: mir_metadatas,
            mir_common.MirStorage.MIR_ANNOTATIONS: mir_annotation,
            mir_common.MirStorage.MIR_KEYWORDS: mir_keywords,
            mir_common.MirStorage.MIR_TASKS: mir_tasks,
        }
        mir_storage_ops.MirStorageOps.save_and_commit(mir_root=mir_root,
                                                      his_branch=(src_revs or "master"),
                                                      mir_branch=dst_typ_rev_tid.rev,
                                                      mir_datas=mir_data,
                                                      commit_message=dst_typ_rev_tid.tid)

        logging.info("import done.")

        return code.MirCode.RC_OK


def _generate_sha_and_cp(index_file, sha_idx_file, sha_folder):
    if not os.path.isfile(index_file):
        logging.error("Invalid input paths")
        return code.MirCode.RC_ERROR_INVALID_ARGS

    os.makedirs(sha_folder, exist_ok=True)

    with open(index_file) as idx_f, open(sha_idx_file, 'w') as sha_f:
        idx = 0
        for line in idx_f:
            media_src = line.strip()
            if not media_src or not os.path.isfile(media_src):
                logging.warning("invalid file: ", media_src)
                continue
            sha1 = hash_utils.sha1sum_for_file(media_src)
            sha_f.writelines("\t".join([sha1, media_src]) + '\n')

            media_dst = os.path.join(sha_folder, sha1)
            if not os.path.isfile(media_dst):
                shutil.copyfile(media_src, media_dst)

            idx += 1
            if idx % 5000 == 0:
                logging.info("finished %d hashes", idx)
    return code.MirCode.RC_OK


def bind_to_subparsers(subparsers, parent_parser):  # pragma: no cover
    importing_arg_parser = subparsers.add_parser("import",
                                                 parents=[parent_parser],
                                                 description="use this command to import data from img/anno folder",
                                                 help="import raw data")
    importing_arg_parser.add_argument("--index-file",
                                      dest="index_file",
                                      type=str,
                                      help="index of input media, one file per line")
    importing_arg_parser.add_argument("--annotation-dir", dest="anno", type=str, help="corresponding annotation folder")
    importing_arg_parser.add_argument("--gen-dir", dest="gen", type=str, help="storage path of generated data files")
    importing_arg_parser.add_argument("--dataset-name",
                                      dest="dataset_name",
                                      type=str,
                                      help="name of the dataset to be created, use tid if not set.")
    importing_arg_parser.add_argument("--src-revs", dest="src_revs", type=str, help="rev: source rev")
    importing_arg_parser.add_argument("--dst-rev",
                                      dest="dst_rev",
                                      type=str,
                                      required=True,
                                      help="rev@tid: destination branch name and task id")
    importing_arg_parser.set_defaults(func=CmdImport)
