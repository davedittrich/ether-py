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
    """Remove solc compiler version(s)"""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.formatter_class = argparse.RawDescriptionHelpFormatter
        parser.add_argument(
            'version',
            metavar='VERSION',
            nargs='+',
            default=['latest'],
            help="Solidity compiler version",
        )
        parser.epilog = textwrap.dedent("""\
            Remove one or more ``solc`` compiler versions.

            Specify one or more compiler versions by their version
            number, by a substring (to select more than one version
            in a series), the word ``latest`` to remove the highest
            numbered version, or ``all`` to remove all versions.

            ::

                $ ether-py solc versions 0.8
                +---------+
                | version |
                +---------+
                | 0.8.3   |
                | 0.8.0   |
                +---------+
                $ ether-py solc remove 0.8.0
                [+] removed /Users/dittrich/.solcx/solc-v0.8.0
                $ ether-py solc versions
                +---------+
                | version |
                +---------+
                | 0.8.3   |
                | 0.7.6   |
                +---------+

            """)  # noqa
        return parser

    def take_action(self, parsed_args):
        self.log.debug('[+] removing solc compiler version(s)')
        installed_versions = [
            str(version)
            for version in solcx.get_installed_solc_versions()
        ]
        installed_versions.sort(reverse=True)
        if 'latest' in parsed_args.version:
            remove_versions = installed_versions[0]
        elif 'all' in parsed_args.version:
            remove_versions = installed_versions
        else:
            remove_versions = parsed_args.version
        for version in remove_versions:
            if version not in installed_versions:
                print(('[-] solidity compiler version '
                       f"'{version}'' is not installed"),
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
