# -*- coding: utf-8 -*-

import argparse
import logging
import solcx
import sys
import textwrap

from ether_py.solc import SOLCX_BINARY_PATH
from cliff.command import Command


class SolcInstall(Command):
    """Install solc compiler version(s)"""

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
            Install one or more ``solc`` compiler versions.

            Solidity smart contracts (``.sol`` files) usually specify a
            particular ``solc`` compiler version, or a range of compatible
            versions, using a ``pragma`` statement that looks like this::

                pragma solidity >=0.6.0 <0.8.0;

            ``ether-py`` will extract the ``pragma`` statement and pass it
            along to ``solc`` when compiling the contract. If no compatible
            compiler can be found, you will get an error message that
            shows the ``pragma`` statement. Select a compiler version that
            matches the range from a list of installable ``solc`` versions
            shown by ``ether-py solc versions --installable`` (``0.7.6`` will
            work in this case.) You can then install it, and the most recent
            compiler version, like this:

            ::

                $ ether-py solc install 0.7.6 latest
                solcx                     INFO     Downloading from https://solc-bin.ethereum.org/macosx-amd64/solc-macosx-amd64-v0.7.6+commit.7338295f
                solcx                     INFO     solc 0.7.6 successfully installed at: /Users/dittrich/.solcx/solc-v0.7.6
                [+] installed solc version '0.7.6'
                solcx                     INFO     Downloading from https://solc-bin.ethereum.org/macosx-amd64/solc-macosx-amd64-v0.8.3+commit.8d00100c
                solcx                     INFO     solc 0.8.3 successfully installed at: /Users/dittrich/.solcx/solc-v0.8.3
                [+] installed solc version 'latest'
                $ ether-py solc versions
                +---------+
                | version |
                +---------+
                | 0.8.3   |
                | 0.8.0   |
                | 0.7.6   |
                +---------+

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
                    print(f"[+] installed solc version '{version}'")

# vim: set ts=4 sw=4 tw=0 et :
