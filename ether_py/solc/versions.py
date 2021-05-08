# -*- coding: utf-8 -*-

import argparse
import logging
import solcx
import textwrap

from cliff.lister import Lister


class SolcVersions(Lister):
    """Show solc compiler versions"""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.formatter_class = argparse.RawDescriptionHelpFormatter
        parser.add_argument(
            '--installable',
            action='store_true',
            dest='installable',
            default=False,
            help='Show installable versions (default: False)'
        )
        parser.add_argument(
            'version',
            metavar='VERSION',
            help="Solidity compiler version",
            nargs='?',
            default=None)
        parser.epilog = textwrap.dedent(f"""\
            Show ``solc`` compiler versions.

            By default, you will be shown the list of ``solc`` compilers
            that are currently installed and available for use in compiling
            Solidity smart contract (``.sol`` files).

            ::

                $ ether-py solc versions
                +---------+
                | version |
                +---------+
                | 0.8.0   |
                | 0.7.6   |
                +---------+


            To instead see a list of installable versions, use the
            ``--installable`` flag.

            ::

                $ ether-py solc versions --installable
                +---------+
                | version |
                +---------+
                | 0.8.3   |
                | 0.8.2   |
                | 0.8.1   |
                | 0.8.0   |
                | 0.7.6   |
                | 0.7.5   |
                |  . . .  |
                | 0.4.12  |
                | 0.4.11  |
                +---------+

            To see a subset of versions, include an argument with the
            substring to match on:

            ::

                $ ether-py solc versions 0.7 --installable
                +---------+
                | version |
                +---------+
                | 0.7.6   |
                | 0.7.5   |
                | 0.7.4   |
                | 0.7.3   |
                | 0.7.2   |
                | 0.7.1   |
                | 0.7.0   |
                +---------+

            See also ``ether-py solc install --help``.
            """)  # noqa
        return parser

    def take_action(self, parsed_args):
        self.log.debug('[+] showing solc versions')
        columns = ['version']
        solc_versions = (
            solcx.get_installable_solc_versions()
            if parsed_args.installable else
            solcx.get_installed_solc_versions()
        )
        data = [
            (str(version),)
            for version in solc_versions
            if (
                parsed_args.version is None
                or str(version).find(parsed_args.version) != -1
            )
        ]
        return (columns, data)


# vim: set ts=4 sw=4 tw=0 et :
