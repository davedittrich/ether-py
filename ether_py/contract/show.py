# -*- coding: utf-8 -*-

import argparse
import arrow
import logging
import os
import sys
import textwrap

from cliff.lister import Lister
from ether_py.utils import (
    ETHERPY_CONTRACTS_DIR,
    VALID_CONTRACT_TYPES,
)


def details_about(contract_name=None, file_type=None):
    """Return a tuple for details about contract files."""
    if contract_name is None:
        return ('File', 'Last_Modified')
    file_name = os.path.join(ETHERPY_CONTRACTS_DIR,
                             f"{contract_name}.{file_type}")
    mtime = None
    try:
        stat_results = os.stat(file_name)
        mtime = str(arrow.get(stat_results.st_mtime))
    except FileNotFoundError:
        pass
    return (file_name, mtime)


class ContractShow(Lister):
    """Show Solidity contract files"""

    # NOTE: This command acts like a ShowOne, but uses a Lister
    # instead.

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.formatter_class = argparse.RawDescriptionHelpFormatter
        parser.add_argument(
            'name',
            metavar='NAME',
            nargs=1,
            default=None,
            help="Solidity contract name",
        )
        choices = [
            t for t in VALID_CONTRACT_TYPES
            if t != 'sol'
        ]
        parser.add_argument(
            'type',
            metavar='TYPE',
            nargs='?',
            choices=choices,
            default=[],
            help="Associated file type",
        )
        parser.epilog = textwrap.dedent("""\
            List Solidity contract files.


            """)  # noqa
        return parser

    def take_action(self, parsed_args):
        self.log.debug('[+] show Solidity files for contract')
        contract_name = parsed_args.name[0]
        columns = details_about()
        details = [
            details_about(contract_name, file_type)
            for file_type in VALID_CONTRACT_TYPES
            if (
                parsed_args.type is None
                or file_type in parsed_args.type
            )
        ]
        data = [
            detail
            for detail in details
            if detail[1] is not None
        ]
        if not len(data):
            if self.app_args.verbose_level > 1:
                sys.exit("[-] no files found for contract name "
                         f"'{contract_name}' in {ETHERPY_CONTRACTS_DIR}")
            else:
                sys.exit(1)
        return (columns, data)


# vim: set ts=4 sw=4 tw=0 et :
