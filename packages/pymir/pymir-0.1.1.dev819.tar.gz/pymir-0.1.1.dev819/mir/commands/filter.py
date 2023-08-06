import datetime
import logging
from typing import Optional, Set

from mir.commands import base
from mir.tools import checker, code, mir_storage, mir_storage_ops, revs_parser
from ymir_proto.gen import mir_entities_pb2 as mirpb
from ymir_proto.gen import mir_common_pb2 as mir_common
from ymir_proto.util import ids


class CmdFilter(base.BaseCommand):
    # private: misc
    def __preds_set_from_str(preds_str: str, cls_mgr: ids.ClassIdManager) -> Set[int]:
        if not preds_str:
            return set()

        return set(cls_mgr.id_for_names(preds_str.split(";")))

    @staticmethod
    def __predefined_preds_match(asset_ids_set: Set[str], mir_keywords: mirpb.MirKeywords,
                                 preds_set: Set[int]) -> Set[str]:
        # if don't need preds filter, returns all
        if not preds_set:
            return asset_ids_set

        matched_asset_ids_set = set()  # type: Set[str]
        for asset_id in asset_ids_set:
            if asset_id not in mir_keywords.keywords:
                continue

            keyids_set = set(mir_keywords.keywords[asset_id].predifined_keyids)
            if not keyids_set:
                continue

            if keyids_set & preds_set:
                matched_asset_ids_set.add(asset_id)
        return matched_asset_ids_set

    @staticmethod
    def __predefined_excludes_match(asset_ids_set: Set[str], mir_keywords: mirpb.MirKeywords,
                                    excludes_set: Set[int]) -> Set[str]:
        # if don't need excludes filter, returns all
        if not excludes_set:
            return asset_ids_set

        matched_asset_ids_set = set()  # type: Set[str]
        for asset_id in asset_ids_set:
            if asset_id in mir_keywords.keywords:
                keyids_set = set(mir_keywords.keywords[asset_id].predifined_keyids)
                if keyids_set & excludes_set:
                    continue
            matched_asset_ids_set.add(asset_id)
        return matched_asset_ids_set

    # public: run cmd
    @staticmethod
    def run_with_args(mir_root: str, in_cis: Optional[str], ex_cis: Optional[str], src_revs: str, dst_rev: str) -> int:
        # check args
        if not in_cis and not ex_cis:
            logging.error("invalid args: no --in_cis (include class keys) and no --ex-cis (exclude class keys)")
            return code.MirCode.RC_ERROR_INVALID_ARGS

        if not src_revs:
            logging.error("invalid args: empty --src-revs")
            return code.MirCode.RC_ERROR_INVALID_ARGS
        src_typ_rev_tid = revs_parser.parse_single_arg_rev(src_revs)
        if not src_typ_rev_tid.rev:
            logging.error(f"invalid args: no rev in --src-revs: {src_typ_rev_tid}")
            return code.MirCode.RC_ERROR_INVALID_ARGS

        if not dst_rev:
            logging.error("invalid args: --dst-rev")
            return code.MirCode.RC_ERROR_INVALID_ARGS
        dst_typ_rev_tid = revs_parser.parse_single_arg_rev(dst_rev)
        if not dst_typ_rev_tid.tid:
            logging.error(f"invalid args: no tid in --dst-rev: {dst_typ_rev_tid}")
            return code.MirCode.RC_ERROR_INVALID_ARGS
        if not dst_typ_rev_tid.rev:
            logging.error(f"invalid args: no rev in --dst-rev: {dst_typ_rev_tid}")
            return code.MirCode.RC_ERROR_INVALID_ARGS

        return_code = checker.check(mir_root)
        if return_code != code.MirCode.RC_OK:
            return return_code

        mir_contents = mir_storage_ops.MirStorageOps.load(mir_root=mir_root,
                                                          mir_branch=src_typ_rev_tid.rev,
                                                          mir_storages=mir_storage.get_all_mir_storage())
        mir_metadatas = mir_contents[mir_common.MirStorage.MIR_METADATAS]
        mir_annotations = mir_contents[mir_common.MirStorage.MIR_ANNOTATIONS]
        mir_keywords = mir_contents[mir_common.MirStorage.MIR_KEYWORDS]
        mir_tasks = mir_contents[mir_common.MirStorage.MIR_TASKS]
        task_id = dst_typ_rev_tid.tid
        base_task_id = mir_annotations.head_task_id

        if task_id in mir_tasks.tasks:
            logging.error(f"invalid args: task id already exists: {task_id}")
            return code.MirCode.RC_ERROR_INVALID_ARGS
        if not base_task_id:
            raise ValueError("no base task id in tasks.mir")

        assert len(mir_annotations.task_annotations.keys()) == 1
        base_task_annotations = mir_annotations.task_annotations[base_task_id]  # type: mirpb.SingleTaskAnnotations

        class_manager = ids.ClassIdManager()
        preds_set = CmdFilter.__preds_set_from_str(in_cis, class_manager)  # type: Set[int]
        excludes_set = CmdFilter.__preds_set_from_str(ex_cis, class_manager)  # type: Set[int]

        asset_ids_set = set(mir_metadatas.attributes.keys())
        logging.info(f"assets count: {len(asset_ids_set)}")
        asset_ids_set = CmdFilter.__predefined_preds_match(asset_ids_set, mir_keywords, preds_set)
        if preds_set:
            logging.info(f"assets count after select: {len(asset_ids_set)}")
        asset_ids_set = CmdFilter.__predefined_excludes_match(asset_ids_set, mir_keywords, excludes_set)
        if excludes_set:
            logging.info(f"assets count after exclude: {len(asset_ids_set)}")

        if not asset_ids_set:
            logging.info("matched nothing with pred: {}, excludes: {}, please try another preds".format(in_cis, ex_cis))
            return code.MirCode.RC_ERROR_INVALID_ARGS

        matched_mir_metadatas = mirpb.MirMetadatas()
        matched_mir_annotations = mirpb.MirAnnotations()
        matched_mir_keywords = mirpb.MirKeywords()

        # generate matched metadatas, annotations and keywords
        for asset_id in asset_ids_set:
            # generate `matched_mir_metadatas`
            asset_attr = mir_metadatas.attributes[asset_id]
            matched_mir_metadatas.attributes[asset_id].CopyFrom(asset_attr)

        joint_ids = asset_ids_set & mir_keywords.keywords.keys()
        for asset_id in joint_ids:
            # generate `matched_mir_keywords`
            matched_mir_keywords.keywords[asset_id].CopyFrom(mir_keywords.keywords[asset_id])

        # generate `matched_mir_annotations`
        joint_ids = asset_ids_set & base_task_annotations.image_annotations.keys()
        for asset_id in joint_ids:
            matched_mir_annotations.task_annotations[task_id].image_annotations[asset_id].CopyFrom(
                base_task_annotations.image_annotations[asset_id])

        # generate matched tasks
        task = mirpb.Task()
        task.type = mir_common.TaskType.TaskTypeFilter
        task.name = f"filter bid: {base_task_id}, tid: {task_id}, select: {in_cis} exclude: {ex_cis}"
        task.base_task_id = base_task_id
        task.task_id = task_id
        task.timestamp = int(datetime.datetime.now().timestamp())
        mir_storage_ops.add_mir_task(mir_tasks, task)

        logging.info("matched: %d, overriding current mir repo", len(matched_mir_metadatas.attributes))

        matched_mir_contents = {
            mir_common.MirStorage.MIR_METADATAS: matched_mir_metadatas,
            mir_common.MirStorage.MIR_ANNOTATIONS: matched_mir_annotations,
            mir_common.MirStorage.MIR_KEYWORDS: matched_mir_keywords,
            mir_common.MirStorage.MIR_TASKS: mir_tasks,
        }

        mir_storage_ops.MirStorageOps.save_and_commit(mir_root=mir_root,
                                                      mir_branch=dst_typ_rev_tid.rev,
                                                      his_branch=src_typ_rev_tid.rev,
                                                      mir_datas=matched_mir_contents,
                                                      commit_message=task.name)

        return code.MirCode.RC_OK

    def run(self):
        logging.debug("command filter: %s", self.args)
        return CmdFilter.run_with_args(
            mir_root=self.args.mir_root,
            in_cis=self.args.in_cis,
            ex_cis=self.args.ex_cis,
            src_revs=self.args.src_revs,
            dst_rev=self.args.dst_rev)


def bind_to_subparsers(subparsers, parent_parser):  # pragma: no cover
    filter_arg_parser = subparsers.add_parser("filter",
                                              parents=[parent_parser],
                                              description="use this command to filter assets",
                                              help="filter assets")
    filter_arg_parser.add_argument("-p", dest="in_cis", type=str, help="type names")
    filter_arg_parser.add_argument("-P", dest="ex_cis", type=str, help="exclusive type names")
    filter_arg_parser.add_argument("--src-revs", dest="src_revs", type=str, help="type:rev@bid")
    filter_arg_parser.add_argument("--dst-rev", dest="dst_rev", type=str, help="rev@tid")
    filter_arg_parser.set_defaults(func=CmdFilter)
