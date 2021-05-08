# -*- coding: utf-8 -*-

import argparse
import logging
import textwrap

from ether_py.utils import (
    to_str,
    ETH_ATTRIBUTES,
)
from cliff.show import ShowOne


class EthShow(ShowOne):
    """Show Ethereum blockchain information"""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.formatter_class = argparse.RawDescriptionHelpFormatter
        parser.add_argument(
            'field',
            metavar='FIELD',
            choices=ETH_ATTRIBUTES,
            nargs='?',
            default=[],
            help="Blockchain metadata field",
        )
        parser.epilog = textwrap.dedent("""\
            Shows attributes about Ethereum blockchain.

            ::

                $ ether-py eth show
                +------------------+--------------------------------------------+
                | Field            | Value                                      |
                +------------------+--------------------------------------------+
                | block_number     | 15                                         |
                | chain_id         | 1337                                       |
                | coinbase         | 0xB9f74d880185873808D363f9295BBC91314B0759 |
                | default_account  | None                                       |
                | default_block    | latest                                     |
                | gas_price        | 20000000000                                |
                | hashrate         | 0                                          |
                | is_async         | False                                      |
                | mining           | True                                       |
                | protocol_version | 63                                         |
                | syncing          | False                                      |
                +------------------+--------------------------------------------+
            """)  # noqa
        return parser

    def take_action(self, parsed_args):
        self.log.debug('[+] showing Ethereum blockchain info')
        columns = []
        data = []
        fields = [f.lower() for f in parsed_args.field]
        for k in ETH_ATTRIBUTES:
            if not len(fields) or k.lower() in fields:
                columns.append(k)
                data.append((to_str(getattr(self.app.w3.eth, k))))
        return (columns, data)


# vim: set ts=4 sw=4 tw=0 et :
