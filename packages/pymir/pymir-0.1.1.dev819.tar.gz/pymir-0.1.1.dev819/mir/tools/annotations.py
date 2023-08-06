import logging
import os
from typing import Tuple

import xml.dom.minidom

from mir.tools import code
from ymir_proto.gen import mir_entities_pb2 as mirpb
from ymir_proto.util import ids


def _get_dom_xml_tag_node(node: xml.dom.minidom.Element, tag_name: str) -> xml.dom.minidom.Element:
    """
    suppose we have the following xml:
    ```
    <blabla>
        <tag1>tag1_value</tag1>
        <tag2>tag2_value</tag2>
    </blabla>
    ```
    and we have node point to <blabla>, we can use this function to get node tag1 and tag2 \n
    if tag not found, returns None
    """
    tag_nodes = node.getElementsByTagName(tag_name)
    if len(tag_nodes) > 0 and len(tag_nodes[0].childNodes) > 0:
        return tag_nodes[0]
    return None


def _get_dom_xml_tag_data(node: xml.dom.minidom.Element, tag_name: str) -> str:
    """
    suppose we have the following xml:
    ```
    <blabla>
        <tag1>tag1_value</tag1>
        <tag2>tag2_value</tag2>
    </blabla>
    ```
    and we have node point to <blabla>, we can use this function to get tag1_value and tag2_value \n
    if tag not found, returns None
    """
    tag_node = _get_dom_xml_tag_node(node, tag_name)
    if tag_node and len(tag_node.childNodes) > 0:
        return tag_node.childNodes[0].data
    return None


def _xml_obj_to_annotation_and_name(obj: xml.dom.minidom.Element,
                                    class_type_manager: ids.ClassIdManager) -> Tuple[mirpb.Annotation, str]:
    """
    generate mirpb.Annotation instance from object node in coco and pascal annotation xml file
    """
    name = _get_dom_xml_tag_data(obj, "name")
    bndbox_node = _get_dom_xml_tag_node(obj, "bndbox")
    xmin = int(float(_get_dom_xml_tag_data(bndbox_node, "xmin")))
    ymin = int(float(_get_dom_xml_tag_data(bndbox_node, "ymin")))
    xmax = int(float(_get_dom_xml_tag_data(bndbox_node, "xmax")))
    ymax = int(float(_get_dom_xml_tag_data(bndbox_node, "ymax")))
    width = xmax - xmin + 1
    height = ymax - ymin + 1

    annotation = mirpb.Annotation()
    annotation.class_id = class_type_manager.id_and_main_name_for_name(name)[0]
    annotation.box.x = xmin
    annotation.box.y = ymin
    annotation.box.w = width
    annotation.box.h = height
    annotation.score = 0
    return annotation


def import_annotations(mir_annotation: mirpb.MirAnnotations, mir_keywords: mirpb.MirKeywords, in_sha1_file: str,
                       annotations_dir_path: str, task_id: str):
    if (not in_sha1_file) or (not annotations_dir_path):
        logging.error("invalid input paths")
        return code.MirCode.RC_ERROR_INVALID_ARGS

    # read type_id_name_dict and type_name_id_dict
    class_type_manager = ids.ClassIdManager()
    logging.info("loaded type id and names: %d", class_type_manager.size())

    image_annotations = mir_annotation.task_annotations[task_id].image_annotations

    assethash_filename_list = []
    with open(in_sha1_file, "r") as in_file:
        for line in in_file.readlines():
            line_components = line.strip().split()
            if not line_components or len(line_components) < 2:
                logging.warning("incomplete line: %s", line)
                continue
            asset_hash, file_name = line_components[0], line_components[1]
            base_file_name = os.path.splitext(os.path.basename(file_name))[0]
            assethash_filename_list.append((asset_hash, base_file_name))

    logging.info("wrting %d annotations", len(assethash_filename_list))

    counter = 0
    cur_max_id = class_type_manager._max_id
    missing_annotations_counter = 0
    for asset_hash, base_file_name in assethash_filename_list:
        annotation_file = os.path.join(annotations_dir_path, base_file_name + '.xml')
        if not os.path.isfile(annotation_file):
            missing_annotations_counter += 1
            continue
        dom_tree = xml.dom.minidom.parse(annotation_file)
        if not dom_tree:
            logging.error("cannot open annotation_file: {}".format(annotation_file))
            return code.MirCode.RC_ERROR_INVALID_ARGS

        single_asset_keyids_set = set()
        collection = dom_tree.documentElement
        objects = collection.getElementsByTagName("object")
        for idx, obj in enumerate(objects):
            annotation = _xml_obj_to_annotation_and_name(obj, class_type_manager)
            annotation.index = idx
            image_annotations[asset_hash].annotations.append(annotation)
            single_asset_keyids_set.add(annotation.class_id)
        mir_keywords.keywords[asset_hash].predifined_keyids[:] = single_asset_keyids_set

        counter += 1
        if counter % 5000 == 0:
            logging.debug("finished %d / %d", counter, len(assethash_filename_list))

    # find extra class ids, save to new file and exit.
    max_id = class_type_manager._max_id
    if max_id > cur_max_id:
        new_ids = [class_type_manager._dirty_id_names_dict[i] for i in range(cur_max_id + 1, max_id + 1)]
        logging.error("\nError: import process abort because new class labels are detected: {}".format(
            ','.join(new_ids)))
        logging.error("new dict file is stored with a .new suffix at: {}".format(class_type_manager._csv_path))
        logging.error("contact ymir-team@intellif.com how to update ids file before continue,")
        logging.error("or use the .new file to replace the previous one a for temp running.")
        class_type_manager.save()
        return code.MirCode.RC_ERROR_INVALID_ARGS

    if missing_annotations_counter > 0:
        logging.warning(f"asset count that have no annotations: {missing_annotations_counter}")

    return code.MirCode.RC_OK
