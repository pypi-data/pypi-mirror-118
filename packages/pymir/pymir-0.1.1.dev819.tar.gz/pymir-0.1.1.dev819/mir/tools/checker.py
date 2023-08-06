import enum
import logging
import os
import sys
from typing import List

from mir.tools import code, mir_repo_utils


@enum.unique
class Prerequisites(enum.IntEnum):
    NOTHING = 0
    IS_INSIDE_GIT_REPO = enum.auto()
    IS_OUTSIDE_GIT_REPO = enum.auto()
    IS_INSIDE_MIR_REPO = enum.auto()
    IS_OUTSIDE_MIR_REPO = enum.auto()
    IS_DIRTY = enum.auto()
    IS_CLEAN = enum.auto()


_DEFAULT_PREREQUISTITES = [Prerequisites.IS_INSIDE_MIR_REPO, Prerequisites.IS_CLEAN]  # type: List[Prerequisites]


# check mir root
def check(mir_root: str, prerequisites: List[Prerequisites] = _DEFAULT_PREREQUISTITES) -> int:
    for item in prerequisites:
        checker_name = "_check_{}".format(item.name.lower())
        checker_func = getattr(sys.modules[__name__], checker_name)
        return_code = checker_func(mir_root)
        if return_code != code.MirCode.RC_OK:
            logging.info("check failed: {}".format(item.name.lower()))
            return return_code
    return code.MirCode.RC_OK


def _check_nothing(mir_root: str) -> int:
    return code.MirCode.RC_OK


def _check_is_inside_git_repo(mir_root: str) -> int:
    return (code.MirCode.RC_OK if os.path.isdir(os.path.join(mir_root, ".git")) else code.MirCode.RC_ERROR_INVALID_ARGS)


def _check_is_outside_git_repo(mir_root: str) -> int:
    return (code.MirCode.RC_OK
            if not os.path.isdir(os.path.join(mir_root, ".git")) else code.MirCode.RC_ERROR_INVALID_ARGS)


def _check_is_inside_mir_repo(mir_root: str) -> int:
    return (code.MirCode.RC_OK if os.path.isdir(os.path.join(mir_root, ".git"))
            and os.path.isdir(os.path.join(mir_root, ".dvc")) else code.MirCode.RC_ERROR_INVALID_MIR_REPO)


def _check_is_outside_mir_repo(mir_root: str) -> int:
    return (code.MirCode.RC_OK if not os.path.isdir(os.path.join(mir_root, ".git"))
            or not os.path.isdir(os.path.join(mir_root, ".dvc")) else code.MirCode.RC_ERROR_INVALID_ARGS)


def _check_is_dirty(mir_root: str) -> int:
    is_dirty = mir_repo_utils.mir_check_repo_dirty(mir_root)
    return code.MirCode.RC_OK if is_dirty else code.MirCode.RC_ERROR_INVALID_ARGS


def _check_is_clean(mir_root: str) -> int:
    is_dirty = mir_repo_utils.mir_check_repo_dirty(mir_root)
    return code.MirCode.RC_OK if not is_dirty else code.MirCode.RC_ERROR_DIRTY_REPO
