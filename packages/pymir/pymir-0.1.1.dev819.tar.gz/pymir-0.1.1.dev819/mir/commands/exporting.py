import logging

from mir.tools import checker, data_exporter, revs_parser, mir_storage_ops
from mir.commands import base
from ymir_proto.gen import mir_common_pb2 as mir_common


class CmdExport(base.BaseCommand):
    def run(self):
        logging.debug(f"command export: {self.args}")

        return CmdExport.run_with_args(mir_root=self.args.mir_root,
                                       asset_dir=self.args.asset_dir,
                                       annotation_dir=self.args.annotation_dir,
                                       media_location=self.args.media_location,
                                       src_revs=self.args.src_revs,
                                       format=self.args.format)

    @staticmethod
    def run_with_args(mir_root: str, asset_dir: str, annotation_dir: str, media_location: str, src_revs: str,
                      format: str):
        # check args
        if not mir_root:
            mir_root = '.'
        if not format:
            format = 'ark'

        if not asset_dir or not annotation_dir:
            logging.error('empty --asset-dir or --annotation-dir')
            return mir_common.RC_CMD_INVALID_ARGS
        if not media_location:
            logging.error('empty --media-location')
            return mir_common.RC_CMD_INVALID_ARGS
        if not src_revs:
            logging.error('empty --src-revs')
            return mir_common.RC_CMD_INVALID_ARGS
        if format and (format not in data_exporter.SUPPORTED_EXPORT_FORMATS):
            logging.error(f"invalid --format: {format}")
            return mir_common.RC_CMD_INVALID_ARGS

        src_typ_rev_tid = revs_parser.parse_single_arg_rev(src_revs)
        if not src_typ_rev_tid.rev:
            logging.error(f"invalid --src-revs: {src_revs}: no rev found")
            return mir_common.RC_CMD_INVALID_ARGS

        return_code = checker.check(mir_root, prerequisites=[checker.Prerequisites.IS_INSIDE_MIR_REPO])
        if return_code != mir_common.RC_OK:
            return return_code

        format_type = data_exporter.format_type_from_str(format)

        # asset ids
        mir_metadatas = mir_storage_ops.MirStorageOps.load_single(mir_root=mir_root,
                                                                  mir_branch=src_typ_rev_tid.rev,
                                                                  ms=mir_common.MIR_METADATAS)
        asset_ids = set(mir_metadatas.attributes.keys())
        if not asset_ids:
            logging.error('nothing to export')
            return mir_common.RC_CMD_INVALID_ARGS

        # export
        data_exporter.export(mir_root=mir_root,
                             assets_location=media_location,
                             class_type_ids=None,
                             asset_ids=asset_ids,
                             asset_dir=asset_dir,
                             annotation_dir=annotation_dir,
                             need_suffix=True,
                             base_branch=src_typ_rev_tid.rev,
                             format_type=format_type)

        return mir_common.RC_OK


def bind_to_subparsers(subparsers, parent_parser):  # pragma: no cover
    exporting_arg_parser = subparsers.add_parser('export',
                                                 parents=[parent_parser],
                                                 description='use this command to export data',
                                                 help='export data')
    exporting_arg_parser.add_argument("--asset-dir",
                                      required=True,
                                      dest="asset_dir",
                                      type=str,
                                      help="export directory for assets")
    exporting_arg_parser.add_argument("--annotation-dir",
                                      required=True,
                                      dest="annotation_dir",
                                      type=str,
                                      help="export directory for annotations")
    exporting_arg_parser.add_argument('--media-location',
                                      dest='media_location',
                                      type=str,
                                      help='location of hashed assets')
    exporting_arg_parser.add_argument('--src-revs',
                                      dest='src_revs',
                                      type=str,
                                      help='rev@bid: source rev and base task id')
    exporting_arg_parser.add_argument('--format',
                                      dest='format',
                                      type=str,
                                      default="ark",
                                      choices=["ark", "voc", "none"],
                                      help='annotation format: ark / voc / none')
    exporting_arg_parser.set_defaults(func=CmdExport)
