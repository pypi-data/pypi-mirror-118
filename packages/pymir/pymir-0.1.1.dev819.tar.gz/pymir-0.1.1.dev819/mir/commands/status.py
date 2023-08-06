import logging
import os

import google.protobuf.json_format as json_format

from mir.commands import base
from mir.tools import checker, code, mir_repo_utils, mir_storage
from ymir_proto.gen import mir_common_pb2 as mir_common
from ymir_proto.gen import mir_entities_pb2 as mirpb


class CmdStatus(base.BaseCommand):
    def run(self):
        logging.debug("command status: %s", self.args)

        return self.run_with_args(mir_root=self.args.mir_root,
                                  va=self.args.va,
                                  vm=self.args.vm,
                                  vk=self.args.vk,
                                  vt=self.args.vt)

    @staticmethod
    def run_with_args(mir_root, va=False, vm=False, vk=False, vt=False):
        return_code = checker.check(mir_root, [checker.Prerequisites.IS_INSIDE_MIR_REPO])
        if return_code != code.MirCode.RC_OK:
            return return_code

        metadata_file = os.path.join(mir_root, mir_storage.mir_path(mir_common.MirStorage.MIR_METADATAS))
        if os.path.isfile(metadata_file):
            with open(metadata_file, "rb") as file:
                mir_metadatas = mirpb.MirMetadatas()
                mir_metadatas.ParseFromString(file.read())
                CmdStatus._show_metadatas(mir_metadatas, vm)
        else:
            logging.warning("metadatas.mir not exist.")

        annotations_file = os.path.join(mir_root, mir_storage.mir_path(mir_common.MirStorage.MIR_ANNOTATIONS))
        if os.path.isfile(annotations_file):
            with open(annotations_file, "rb") as file:
                mir_annotations = mirpb.MirAnnotations()
                mir_annotations.ParseFromString(file.read())  # TODO: VERY SLOW IN ParseFromString
                CmdStatus._show_annotations(mir_annotations, va)
        else:
            logging.warning("annotations.mir not exist.")

        keywords_file = os.path.join(mir_root, mir_storage.mir_path(mir_common.MirStorage.MIR_KEYWORDS))
        if os.path.isfile(keywords_file):
            with open(keywords_file, "rb") as file:
                mir_keywords = mirpb.MirKeywords()
                mir_keywords.ParseFromString(file.read())
                CmdStatus._show_keywords(mir_keywords, vk)
        else:
            logging.warning("keywords.mir not exist.")

        tasks_file = os.path.join(mir_root, mir_storage.mir_path(mir_common.MirStorage.MIR_TASKS))
        if os.path.isfile(tasks_file):
            with open(tasks_file, "rb") as file:
                mir_tasks = mirpb.MirTasks()
                mir_tasks.ParseFromString(file.read())
                CmdStatus._show_tasks(mir_tasks, vt)
        else:
            logging.warning("tasks.mir not exist.")

        repo_dirty = mir_repo_utils.mir_check_repo_dirty(mir_root=mir_root)
        if repo_dirty:
            logging.info("repo: dirty")
        else:
            logging.info("repo: clean")

        return code.MirCode.RC_OK

    @staticmethod
    def _show_metadatas(mir_metadatas: mirpb.MirMetadatas, verbose: bool):
        logging.info("metadatas.mir: assets: %d", len(mir_metadatas.attributes))
        if verbose:
            logging.info(json_format.MessageToDict(mir_metadatas))

    @staticmethod
    def _show_annotations(mir_annotations: mirpb.MirAnnotations, verbose: bool):
        logging.info("annotations.mir: %d", len(mir_annotations.task_annotations))
        for task_id, task_annotations in mir_annotations.task_annotations.items():
            logging.info("  task: %s: images: %d",
                         task_id, len(task_annotations.image_annotations))
            if verbose:
                logging.info(json_format.MessageToDict(mir_annotations))

    @staticmethod
    def _show_keywords(mir_keywords: mirpb.MirKeywords, verbose: bool):
        logging.info("keywords.mir: assets: %d", len(mir_keywords.keywords))
        if verbose:
            logging.info(json_format.MessageToDict(mir_keywords))

    @staticmethod
    def _show_tasks(mir_tasks: mirpb.MirTasks, verbose: bool):
        logging.info("tasks.mir: tasks: %d", len(mir_tasks.tasks))
        if verbose:
            logging.info(json_format.MessageToDict(mir_tasks))


def bind_to_subparsers(subparsers, parent_parser):  # pragma: no cover
    status_arg_parser = subparsers.add_parser("status",
                                              parents=[parent_parser],
                                              description="use this command to show current workspace status",
                                              help="show current workspace status")
    status_arg_parser.add_argument("--vm", dest="vm", action="store_true", help="show metadatas details")
    status_arg_parser.add_argument("--va", dest="va", action="store_true", help="show annotations details")
    status_arg_parser.add_argument("--vk", dest="vk", action="store_true", help="show keywords details")
    status_arg_parser.add_argument("--vt", dest="vt", action="store_true", help="show tasks details")
    status_arg_parser.set_defaults(func=CmdStatus)
