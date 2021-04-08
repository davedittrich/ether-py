# -*- coding: utf-8 -*-

import argparse
import logging
import solcx
import textwrap

# from . import SOLCX_BINARY_PATH
from cliff.lister import Lister


class SolcVersions(Lister):
    """Show solc-x installed versions."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.formatter_class = argparse.RawDescriptionHelpFormatter
        parser.add_argument(
            '--installable',
            action='store_true',
            dest='installable',
            default=False,
            help=('Show installable versions (default: False)')
        )
        parser.add_argument(
            'version',
            nargs='?',
            default=None)
        parser.epilog = textwrap.dedent(f"""\
            Show ``solc`` compiler versions.

            By default, you will be shown the list of ``solc``
            compilers that are installed.

            ::

                $ ether-py solc versions

            To instead see a list of installable versions, add the
            ``--installable`` flag.

            See also ``ether-py solc install --help``.
            """)  # noqa
        return parser

    def take_action(self, parsed_args):
        self.log.debug('[+] showing solc-x versions')
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
                or version.find(parsed_args.version) > 0
            )
        ]
        return (columns, data)


# vim: set ts=4 sw=4 tw=0 et :
