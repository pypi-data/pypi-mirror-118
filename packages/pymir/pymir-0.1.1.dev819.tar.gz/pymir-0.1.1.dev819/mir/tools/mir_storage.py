from typing import List

from google.protobuf import message as pb_message

from ymir_proto.gen import mir_common_pb2 as mir_common
from ymir_proto.gen import mir_entities_pb2 as mirpb


def mir_type(mir_storage: mir_common.MirStorage):
    MIR_TYPE = {
        mir_common.MirStorage.MIR_METADATAS: mirpb.MirMetadatas,
        mir_common.MirStorage.MIR_ANNOTATIONS: mirpb.MirAnnotations,
        mir_common.MirStorage.MIR_KEYWORDS: mirpb.MirKeywords,
        mir_common.MirStorage.MIR_TASKS: mirpb.MirTasks,
    }
    return MIR_TYPE[mir_storage]


def mir_path(mir_storage: mir_common.MirStorage):
    MIR_PATH = {
        mir_common.MirStorage.MIR_METADATAS: 'metadatas.mir',
        mir_common.MirStorage.MIR_ANNOTATIONS: 'annotations.mir',
        mir_common.MirStorage.MIR_KEYWORDS: 'keywords.mir',
        mir_common.MirStorage.MIR_TASKS: 'tasks.mir',
    }
    return MIR_PATH[mir_storage]


def get_all_mir_paths():
    return [mir_path(ms) for ms in get_all_mir_storage()]


def get_all_mir_storage() -> List[pb_message.Message]:
    return [
        mir_common.MirStorage.MIR_METADATAS,
        mir_common.MirStorage.MIR_ANNOTATIONS,
        mir_common.MirStorage.MIR_KEYWORDS,
        mir_common.MirStorage.MIR_TASKS,
    ]
