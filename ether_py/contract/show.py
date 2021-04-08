# -*- coding: utf-8 -*-

import argparse
import logging
import textwrap

from cliff.show import ShowOne
from ether_py.utils import (
    ETHERPY_CONTRACTS_DIR,
    VALID_CONTRACT_TYPES,
)


class ContractShow(ShowOne):
    """Show Solidity contract files"""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.formatter_class = argparse.RawDescriptionHelpFormatter
        parser.add_argument(
            'name',
            nargs=1,
            default=None)
        choices = [
            t for t in VALID_CONTRACT_TYPES
            if t != 'sol'
        ]
        parser.add_argument(
            'type',
            nargs='?',
            choices=choices,
            default=[])
        parser.epilog = textwrap.dedent("""\
            Show Solidity contract files.


            """)  # noqa
        return parser

    def take_action(self, parsed_args):
        self.log.debug('[+] showing Solidity contract files')
        contact_name = parsed_args.name[0]
        columns = []
        data = []
        return (columns, data)


# vim: set ts=4 sw=4 tw=0 et :
