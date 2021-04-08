# -*- coding: utf-8 -*-

import argparse
import logging
import os
import solcx
import sys
import textwrap

from ether_py.solc import SOLCX_BINARY_PATH
from cliff.command import Command


class SolcRemove(Command):
    """Remove solc-x compiler version(s)."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.formatter_class = argparse.RawDescriptionHelpFormatter
        parser.add_argument(
            'version',
            nargs='+',
            default=['latest'])
        parser.epilog = textwrap.dedent("""\
            Remove one or more ``solc`` compiler versions.

            ::

                $ ether-py solc remove 0.8.0

            """)  # noqa
        return parser

    def take_action(self, parsed_args):
        self.log.debug('[+] removing solc compiler version(s)')
        installed_versions = [
            str(version)
            for version in solcx.get_installed_solc_versions()
        ]
        for version in parsed_args.version:
            if version not in installed_versions:
                print(('[-] solidity compiler version '
                       f'{version} is not installed'),
                      file=sys.stderr)
            else:
                compiler_path = os.path.join(
                    SOLCX_BINARY_PATH,
                    f"solc-v{version}"
                )
                if self.app_args.verbose_level > 1:
                    print(f'[+] removing solc compiler version {version}')
                os.unlink(compiler_path)
                if self.app_args.verbose_level == 1:
                    print(f'[+] removed {compiler_path}')


# vim: set ts=4 sw=4 tw=0 et :
