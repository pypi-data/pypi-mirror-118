import logging

from mir import scm
from mir.commands import base
from mir.tools import checker, code


class CmdBranch(base.BaseCommand):
    @staticmethod
    def run_with_args(mir_root: str, remote: bool, delete: str, force_delete: str) -> int:
        return_code = checker.check(mir_root, [checker.Prerequisites.IS_INSIDE_MIR_REPO])
        if return_code != code.MirCode.RC_OK:
            return return_code

        # can not delete master branch
        if delete and force_delete:
            return code.MirCode.RC_ERROR_INVALID_ARGS
        if delete == "master" or force_delete == "master":
            logging.info("can not delete master branch")
            return code.MirCode.RC_ERROR_INVALID_BRANCH_OR_TAG

        cmd_opts = []
        if remote:
            cmd_opts.append("--remote")
        elif delete:
            cmd_opts.extend(["-d", delete])
        elif force_delete:
            cmd_opts.extend(["-D", force_delete])

        repo_git = scm.Scm(mir_root, scm_executable="git")
        output_str = repo_git.branch(cmd_opts)
        if output_str:
            logging.info("\n%s" % output_str)

        return code.MirCode.RC_OK

    def run(self):
        logging.debug("command branch: %s" % self.args)

        return CmdBranch.run_with_args(mir_root=self.args.mir_root,
                                       remote=False,
                                       delete=self.args.delete,
                                       force_delete=self.args.force_delete)


def bind_to_subparsers(subparsers, parent_parser):  # pragma: no cover
    branch_arg_parser = subparsers.add_parser("branch",
                                              parents=[parent_parser],
                                              description="use this command to show mir repo branches",
                                              help="show mir repo branches")
    delete_group = branch_arg_parser.add_mutually_exclusive_group()
    group = delete_group.add_mutually_exclusive_group()
    group.add_argument("-d", dest="delete", type=str, help="delete branch, if branch not merged, raise errors")
    group.add_argument("-D", dest="force_delete", type=str, help="delete branch, even if branch not merged")
    branch_arg_parser.set_defaults(func=CmdBranch)
