"""
exports the assets and annotations from mir format to ark-training-format
"""

from enum import Enum
import logging
import os
from typing import Dict, List, Optional, Set, Tuple
import xml.etree.ElementTree as ElementTree

from mir.tools import mir_storage_ops
from mir.tools import utils as mir_utils
from ymir_proto.gen import mir_common_pb2 as mir_common
from ymir_proto.gen import mir_entities_pb2 as mirpb
from ymir_proto.util import ids


class ExportError(Exception):
    """
    exception type raised by function `export`
    """
    pass


class ExportFormat(str, Enum):
    EXPORT_FORMAT_UNKNOWN = 'unknown'
    EXPORT_FORMAT_NO_ANNOTATION = 'none'
    EXPORT_FORMAT_ARK = 'ark'
    EXPORT_FORMAT_VOC = 'voc'


# public: format type
SUPPORTED_EXPORT_FORMATS = {
    ExportFormat.EXPORT_FORMAT_NO_ANNOTATION.value, ExportFormat.EXPORT_FORMAT_ARK.value,
    ExportFormat.EXPORT_FORMAT_VOC.value
}


def format_type_from_str(format: str) -> ExportFormat:
    return ExportFormat(format.lower())


# public: export
def export(mir_root: str, assets_location: str, class_type_ids: Set[int], asset_ids: str, asset_dir: str,
           annotation_dir: str, need_suffix: bool, base_branch: str,
           format_type: ExportFormat) -> bool:
    """
    export assets and annotations

    Args:
        mir_root (str): path to mir repo root directory
        assets_location (str): path to assets storage directory
        class_type_ids (Set[int]): class ids, all objects within this set will be exported, if None, export everything
        asset_ids (Set[str]): export asset ids
        asset_dir (str): asset directory
        annotation_dir (str): annotation directory, if format_type is NO_ANNOTATION, this could be None
        need_suffix (str): if true, all export assets will have it's type as suffix, jpg, png, etc.
        base_branch (str): data branch
        format_type (ExportFormat): format type, NONE means exports no annotations

    Raises:
        ValueError: if mir repo not provided

    Returns:
        True if export finished, raises errors when failed
    """
    if not mir_root:
        raise ValueError("invalid mir_repo")

    # export assets
    os.makedirs(asset_dir, exist_ok=True)
    asset_result = mir_utils.store_assets_to_dir(asset_ids=asset_ids,
                                                 out_root=asset_dir,
                                                 sub_folder=".",
                                                 asset_location=assets_location,
                                                 overwrite=False,
                                                 create_prefix=False,
                                                 need_suffix=need_suffix)

    logging.info(f"export {len(asset_result)} assets out of {len(asset_ids)}")

    if format_type == ExportFormat.EXPORT_FORMAT_NO_ANNOTATION:
        return True

    # export annotations
    mir_datas = mir_storage_ops.MirStorageOps.load(
        mir_root=mir_root,
        mir_branch=base_branch,
        mir_storages=[mir_common.MirStorage.MIR_METADATAS, mir_common.MirStorage.MIR_ANNOTATIONS])
    mir_annotations = mir_datas[mir_common.MirStorage.MIR_ANNOTATIONS]

    # add all annotations to assets_to_det_annotations_dict
    # key: asset_id as str, value: annotations as List[mirpb.Annotation]
    assets_to_det_annotations_dict = _annotations_by_assets(mir_annotations=mir_annotations,
                                                            class_type_ids=class_type_ids,
                                                            base_task_id=mir_annotations.head_task_id)

    if format_type == ExportFormat.EXPORT_FORMAT_ARK:
        _export_detect_ark_annotations_to_path(annotations_dict=assets_to_det_annotations_dict,
                                               asset_ids=asset_ids,
                                               dest_path=annotation_dir)
    elif format_type == ExportFormat.EXPORT_FORMAT_VOC:
        mir_metadatas = mir_datas[mir_common.MirStorage.MIR_METADATAS]
        _export_detect_voc_annotations_to_path(annotations_dict=assets_to_det_annotations_dict,
                                               mir_metadatas=mir_metadatas,
                                               asset_ids=asset_ids,
                                               dest_path=annotation_dir)
    else:
        raise ValueError(f"unsupported format: {format_type.name}")

    return True


def generate_asset_index_file(asset_dir: str, rel_start_dir: str, index_file_path: str,
                              image_suffixes: tuple = ('.jpg', '.jpeg', '.png')):
    """
    generate index file for export result.

    in index file, each line is a relpath start from dir or index_file_path, and points to export asset file

    examples:
        assets_dir is /tmp/assets, and rel_start_dir is /tmp \n
        then index file should be something like: \n
        assets/sha1sum-1.jpg \n
        assets/sha1sum-2.jpg

    Args:
        asset_dir (str): asset dir, every jpg / jpeg / png inside this dir will export to index.tsv
        rel_start_dir (str): start point of relative path, should exists
        index_file_path (str): path to index file you want to generate, should not exists
        image_suffixes (tuple): available image suffixes

    Raises:
        ValueError: if export_result, asset_dir or index_file_path empty
        ValueError: if index_file_path exists
        ValueError: if asset_id in export_result does not have an asset file name
    """
    if not asset_dir or not index_file_path or not image_suffixes:
        raise ValueError('invalid args')
    if not os.path.isdir(asset_dir):
        raise ValueError(f"invalid asset_dir: {asset_dir}, not a directory")
    if not os.path.isdir(rel_start_dir):
        raise ValueError(f"invalid rel_start_dir: {rel_start_dir}, not a directory")
    if os.path.exists(index_file_path):
        raise ValueError(f"index file already exists: {index_file_path}")

    index_dir = os.path.dirname(index_file_path)
    os.makedirs(index_dir, exist_ok=True)  # make sure that this dir exists

    relpath = os.path.relpath(asset_dir, start=rel_start_dir)

    with open(index_file_path, 'w') as idx_f:
        for item in os.listdir(asset_dir):
            if not os.path.isfile(os.path.join(asset_dir, item)) or os.path.splitext(item)[1] not in image_suffixes:
                continue
            idx_f.write(os.path.join(relpath, item) + '\n')


# private: export annotations: general
def _annotations_by_assets(mir_annotations: mirpb.MirAnnotations, class_type_ids: Set[int],
                           base_task_id: str) -> Dict[str, List[mirpb.Annotation]]:
    """
    get annotations by assets

    Args:
        mir_annotations (mirpb.MirAnnotations): annotations
        class_type_ids (Set[int]): only type ids within it could be output, if None, no class id filter applied
        base_task_id (str): base task id

    Returns:
        Dict, key: asset id, value: List[mirpb.Annotation]
    """
    assets_to_det_annotations_dict = {}  # type: Dict[str, List[mirpb.Annotation]]

    if base_task_id not in mir_annotations.task_annotations:
        raise ValueError(f"base task id: {base_task_id} not in mir_annotations")

    task_annotations = mir_annotations.task_annotations[base_task_id]
    for asset_id, image_annotations in task_annotations.image_annotations.items():
        matched_annotations = [
            annotation for annotation in image_annotations.annotations
            if (not class_type_ids or (annotation.class_id in class_type_ids))
        ]
        assets_to_det_annotations_dict[asset_id] = matched_annotations

    return assets_to_det_annotations_dict


# private: export annotations: ark
def _export_detect_ark_annotations_to_path(annotations_dict: Dict[str, List[mirpb.Annotation]], asset_ids: Set[str],
                                           dest_path: str) -> None:
    if not asset_ids:
        raise ValueError("empty asset ids")

    os.makedirs(dest_path, exist_ok=True)

    missing_counter = 0
    empty_counter = 0
    for asset_id in asset_ids:
        if asset_id not in annotations_dict:
            missing_counter += 1
            continue
        annotations = annotations_dict[asset_id]
        if len(annotations) == 0:
            empty_counter += 1
            continue

        file_name = f"{asset_id}.txt"
        dest_file_path = os.path.join(dest_path, file_name)
        _single_image_annotations_to_ark(annotations, dest_file_path)

    if missing_counter > 0 or empty_counter > 0:
        logging.warning(f"missing annotations assets: {missing_counter}, "
                        f"empty annotations assets: {empty_counter} out of {len(asset_ids)}")


# private: export annotations: voc
def _export_detect_voc_annotations_to_path(annotations_dict: Dict[str, List[mirpb.Annotation]],
                                           mir_metadatas: mirpb.MirMetadatas, asset_ids: Set[str],
                                           dest_path: str) -> None:
    if not asset_ids:
        raise ValueError('empty asset_ids')
    if not mir_metadatas:
        raise ValueError('invalid mir_metadatas')

    os.makedirs(dest_path, exist_ok=True)

    cls_id_mgr = ids.ClassIdManager()

    missing_counter = 0
    empty_counter = 0
    for asset_id in asset_ids:
        if asset_id not in mir_metadatas.attributes:
            raise ValueError(f"can not find asset id: {asset_id} in mir_metadatas")

        if asset_id not in annotations_dict:
            missing_counter += 1
            continue
        annotations = annotations_dict[asset_id]
        if len(annotations) == 0:
            empty_counter += 1
            continue

        attrs = mir_metadatas.attributes[asset_id]
        annotations = annotations_dict[asset_id]

        file_name = f"{asset_id}.xml"
        dest_file_path = os.path.join(dest_path, file_name)
        _single_image_annotations_to_voc(asset_id, attrs, annotations, dest_file_path, cls_id_mgr)

    if missing_counter > 0:
        logging.warning(f"missing annotations assets: {missing_counter}, empty annotations assets: {empty_counter}")


def _single_image_annotations_to_ark(annotations, dest_file_path):
    with open(dest_file_path, "w") as f:
        for annotation in annotations:
            f.write(f"{annotation.class_id}, {annotation.box.x}, {annotation.box.y}, "
                    f"{annotation.box.x + annotation.box.w - 1}, {annotation.box.y + annotation.box.h - 1}\n")


def _single_image_annotations_to_voc(asset_id, attrs, annotations, dest_file_path, cls_id_mgr):
    # annotation
    annotation_node = ElementTree.Element('annotation')

    # annotation: folder
    folder_node = ElementTree.SubElement(annotation_node, 'folder')
    folder_node.text = 'folder'

    # annotation: filename
    filename_node = ElementTree.SubElement(annotation_node, 'filename')
    filename_node.text = asset_id

    # annotation: source
    source_node = ElementTree.SubElement(annotation_node, 'source')

    # annotation: source: database
    database_node = ElementTree.SubElement(source_node, 'database')
    database_node.text = attrs.dataset_name or 'unknown'

    # annotation: source: annotation
    annotation2_node = ElementTree.SubElement(source_node, 'annotation')
    annotation2_node.text = 'unknown'

    # annotation: source: image
    image_node = ElementTree.SubElement(source_node, 'image')
    image_node.text = 'unknown'

    # annotation: size
    size_node = ElementTree.SubElement(annotation_node, 'size')

    # annotation: size: width
    width_node = ElementTree.SubElement(size_node, 'width')
    width_node.text = str(attrs.width)

    # annotation: size: height
    height_node = ElementTree.SubElement(size_node, 'height')
    height_node.text = str(attrs.height)

    # annotation: size: depth
    depth_node = ElementTree.SubElement(size_node, 'depth')
    depth_node.text = str(attrs.image_channels)

    # annotation: segmented
    segmented_node = ElementTree.SubElement(annotation_node, 'segmented')
    segmented_node.text = '0'

    # annotation: object(s)
    for annotation in annotations:
        object_node = ElementTree.SubElement(annotation_node, 'object')

        name_node = ElementTree.SubElement(object_node, 'name')
        name_node.text = cls_id_mgr.main_name_for_id(annotation.class_id) or 'unknown'

        pose_node = ElementTree.SubElement(object_node, 'pose')
        pose_node.text = 'unknown'

        truncated_node = ElementTree.SubElement(object_node, 'truncated')
        truncated_node.text = 'unknown'

        occluded_node = ElementTree.SubElement(object_node, 'occluded')
        occluded_node.text = '0'

        bndbox_node = ElementTree.SubElement(object_node, 'bndbox')

        xmin_node = ElementTree.SubElement(bndbox_node, 'xmin')
        xmin_node.text = str(annotation.box.x)

        ymin_node = ElementTree.SubElement(bndbox_node, 'ymin')
        ymin_node.text = str(annotation.box.y)

        xmax_node = ElementTree.SubElement(bndbox_node, 'xmax')
        xmax_node.text = str(annotation.box.x + annotation.box.w - 1)

        ymax_node = ElementTree.SubElement(bndbox_node, 'ymax')
        ymax_node.text = str(annotation.box.y + annotation.box.h - 1)

        difficult_node = ElementTree.SubElement(object_node, 'difficult')
        difficult_node.text = '0'

    # write to xml
    tree = ElementTree.ElementTree(annotation_node)
    tree.write(dest_file_path, encoding='utf-8')
