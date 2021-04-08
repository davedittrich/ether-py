# -*- coding: utf-8 -*-

import argparse
import logging
import textwrap
import solcx
import sys

from cliff.show import ShowOne


class SolcShow(ShowOne):
    """Show solc compiler information."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.formatter_class = argparse.RawDescriptionHelpFormatter
        parser.add_argument(
            'field',
            nargs='?',
            default=[])
        parser.epilog = textwrap.dedent("""\
            Show ``solc`` compiler information.

            ::

                $ ether-py solc show

            """)  # noqa
        return parser

    def take_action(self, parsed_args):
        self.log.debug('[+] showing solc compiler information')
        try:
            solc_version = str(solcx.get_solc_version(with_commit_hash=False))
            solc_version_with_hash = str(solcx.get_solc_version(with_commit_hash=True))
            solc_executable = str(solcx.install.get_executable())
            solc_installed_versions = ",".join(
                [
                    str(v)
                    for v in solcx.get_installed_solc_versions()
                ]
            )
        except Exception as err:
            sys.exit(" ".join(err.args))
        columns = ['active_version', 'active_version_hash', 'executable', 'installed_versions']
        data = [
            solc_version,
            solc_version_with_hash,
            solc_executable,
            solc_installed_versions,
        ]
        return (columns, data)


# vim: set ts=4 sw=4 tw=0 et :
