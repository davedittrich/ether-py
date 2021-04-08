# -*- coding: utf-8 -*-

import argparse
import logging
import solcx
import sys
import textwrap

from ether_py.solc import SOLCX_BINARY_PATH
from cliff.command import Command


class SolcInstall(Command):
    """Install solc-x compiler version(s)."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.formatter_class = argparse.RawDescriptionHelpFormatter
        parser.add_argument(
            'version',
            nargs='+',
            default=['latest'])
        parser.epilog = textwrap.dedent("""\
            Install one or more ``solc`` compiler versions.

            When you attempt to compile a Solidity smart contract,
            a compiler matching the pragma specified in the ``.sol``
            file will be selected. If none is available, you
            will get an error message showing something like
            this: ``pragma solidity >=0.6.0 <0.8.0;``

            Select a compiler version matching the range specified
            from a list of installable ``solc`` versions shown by
            ``ether-py solc versions --installable``.

            ::

                $ ether-py solc install 0.7.7 0.8.0

            """)  # noqa
        return parser

    def take_action(self, parsed_args):
        self.log.debug('[+] installing solc compiler version(s)')
        installed_versions = [
            str(version)
            for version in solcx.get_installed_solc_versions()
        ]
        installable_versions = [
            str(version)
            for version in solcx.get_installable_solc_versions()
        ]
        for version in parsed_args.version:
            if version in installed_versions:
                print(('[-] solidity compiler version '
                       f'{version} is already installed'),
                      file=sys.stderr)
            elif (
                version != 'latest'
                and version not in installable_versions
            ):
                print(('[-] solidity compiler version '
                       f'{version} is not installable'),
                      file=sys.stderr)
            else:
                show_progress = (
                    self.app_args.verbose_level > 1
                    or self.app.options.debug
                )
                solcx.install_solc(version=version,
                                   show_progress=show_progress,
                                   solcx_binary_path=SOLCX_BINARY_PATH)
                if self.app_args.verbose_level == 1:
                    print(f'[+] installed solc version {version}')

# vim: set ts=4 sw=4 tw=0 et :
