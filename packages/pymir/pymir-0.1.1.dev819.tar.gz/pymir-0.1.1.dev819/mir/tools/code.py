from enum import IntEnum, auto


class MirCode(IntEnum):
    # everything is ok, command finished without any errors or warnings
    RC_OK = 0

    # errors: command failed for some reasons
    # error codes increase from 1
    RC_ERROR_UNKNOWN = auto()  # unknown error(s) occured while command executed
    RC_ERROR_INVALID_MIR_REPO = auto()  # mir command was not invoked inside a mir repo directory
    RC_ERROR_INVALID_ARGS = auto()  # lack of necessary command args, or unexpected operations detected
    RC_ERROR_INVALID_BRANCH_OR_TAG = auto()  # invalid branch name or tag name
    RC_ERROR_INVALID_MIR_FILE = auto()  # files like metadatas.mir, annotations.mir is not valid
    RC_ERROR_INVALID_COMMAND = auto()  # unknown command or sub command
    RC_ERROR_MIR_FILE_NOT_FOUND = auto()  # can not find some mir files
    RC_ERROR_CONFLICTS_OCCURED = auto()  # conflicts detected when mir pull or mir merge
    RC_ERROR_EMPTY_METADATAS = auto()  # no assets found in metadatas.mir
    RC_ERROR_EMPTY_TRAIN_SET = auto()  # no training set when training
    RC_ERROR_EMPTY_VAL_SET = auto()  # no validation set when training
    RC_ERROR_DIRTY_REPO = auto()  # no validation set when training
    RC_ERROR_NOTHING_TO_MERGE = auto()
