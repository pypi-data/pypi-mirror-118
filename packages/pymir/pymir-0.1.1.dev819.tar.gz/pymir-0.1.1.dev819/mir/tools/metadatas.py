import imghdr
import logging
import os
import time
from PIL import Image, ImageFile
from typing import Optional, Tuple

from mir.tools.code import MirCode
from ymir_proto.gen import mir_entities_pb2 as mirpb
from ymir_proto.gen import mir_common_pb2 as mir_common


ImageFile.LOAD_TRUNCATED_IMAGES = True


def _generate_metadata_mir_pb(mir_metadatas: mirpb.MirMetadatas, dataset_name: str, sha1s: list,
                              hashed_asset_root: str) -> MirCode:
    """
    generate mirpb.MirMetadatas from sha1s
    """
    current_timestamp = int(time.time())  # this is a fake timestamp
    timestamp = mirpb.Timestamp()
    timestamp.start = current_timestamp
    timestamp.duration = 0  # image has no duraton

    for val in sha1s:
        metadata_attributes = mirpb.MetadataAttributes()
        metadata_attributes.timestamp.CopyFrom(timestamp)
        metadata_attributes.dataset_name = dataset_name

        # read file
        # if any exception occured, exit without any handler
        hashed_asset_path = os.path.join(hashed_asset_root, val)
        metadata_attributes.asset_type = _type_for_asset(hashed_asset_path)
        whcd = _shape_for_image(hashed_asset_path)
        if whcd:
            metadata_attributes.width = whcd[0]
            metadata_attributes.height = whcd[1]
            metadata_attributes.image_channels = whcd[2]

        mir_metadatas.attributes[val].CopyFrom(metadata_attributes)
    return MirCode.RC_OK


_ASSET_TYPE_STR_TO_ENUM_MAPPING = {
    "jpeg": mir_common.AssetTypeImageJpeg,
    "jpg": mir_common.AssetTypeImageJpeg,
    "png": mir_common.AssetTypeImagePng,
}


def _type_for_asset(asset_path: str) -> int:
    if not asset_path:
        return 0

    asset_type_str = imghdr.what(asset_path)
    if asset_type_str in _ASSET_TYPE_STR_TO_ENUM_MAPPING:
        return _ASSET_TYPE_STR_TO_ENUM_MAPPING[asset_type_str]
    else:
        return mir_common.AssetTypeUnknown


def _shape_for_image(image_asset_path: str) -> Optional[Tuple[int, int, int]]:
    """
    width, height, channels for image asset
    """
    image = Image.open(image_asset_path)
    width, height = image.size
    channel = len(image.split())
    return (width, height, channel)


def import_metadatas(mir_metadatas: mirpb.MirMetadatas, dataset_name: str, in_sha1_path: str,
                     hashed_asset_root: str) -> MirCode:
    # if not enough args, abort
    if (not in_sha1_path or not dataset_name or not hashed_asset_root):
        logging.error("invalid input paths")
        return MirCode.RC_ERROR_INVALID_ARGS

    if mir_metadatas is None:
        # some errors occured, show error message
        logging.critical("mir file is invalid, exit")
        return MirCode.RC_ERROR_INVALID_MIR_REPO

    # read sha1
    sha1s = []
    with open(in_sha1_path, "r") as in_file:
        for line in in_file.readlines():
            if not line or not line.strip():
                continue
            line_components = line.strip().split()
            if not line_components[0]:
                continue
            sha1s.append(line_components[0])
    if not sha1s:
        logging.critical("no sha1s found, exit")
        return MirCode.RC_ERROR_INVALID_ARGS

    # generate mir_metadatas
    ret = _generate_metadata_mir_pb(mir_metadatas=mir_metadatas,
                                    dataset_name=dataset_name,
                                    sha1s=sha1s,
                                    hashed_asset_root=hashed_asset_root)
    return ret
