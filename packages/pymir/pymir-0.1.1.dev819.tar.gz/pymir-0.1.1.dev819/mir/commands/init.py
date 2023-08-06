import logging

from mir import scm
from mir.commands import base
from mir.tools import checker, code


class CmdInit(base.BaseCommand):
    @staticmethod
    def run_with_args(mir_root):
        return_code = checker.check(
            mir_root, [checker.Prerequisites.IS_OUTSIDE_GIT_REPO, checker.Prerequisites.IS_OUTSIDE_MIR_REPO])
        if return_code != code.MirCode.RC_OK:
            return return_code

        repo_git = scm.Scm(root_dir=mir_root, scm_executable='git')
        repo_dvc = scm.Scm(root_dir=mir_root, scm_executable='dvc')
        repo_git.init()
        repo_dvc.init()

        repo_git.commit(["-m", "first commit"])

        return code.MirCode.RC_OK

    def run(self):
        logging.debug("command init: %s", self.args)

        return self.run_with_args(mir_root=self.args.mir_root)


def bind_to_subparsers(subparsers, parent_parser):  # pragma: no cover
    init_arg_parser = subparsers.add_parser("init",
                                            parents=[parent_parser],
                                            description="use this command to init mir repo",
                                            help="init mir repo")
    init_arg_parser.set_defaults(func=CmdInit)
