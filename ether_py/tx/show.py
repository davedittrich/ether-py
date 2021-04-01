# -*- coding: utf-8 -*-

import argparse
import logging
import textwrap
import sys

from ether_py.utils import to_str
from cliff.show import ShowOne


class TxShow(ShowOne):
    """Show Ethereum transaction."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.formatter_class = argparse.RawDescriptionHelpFormatter
        parser.add_argument(
            'tx',
            nargs=1,
            default=None)
        parser.add_argument(
            'field',
            nargs='?',
            default=[])
        parser.epilog = textwrap.dedent("""\
            Show an Ethereum transaction (tx).

            The transaction is identified by hash.

            ::

                $ ether-py tx show 0xf357f2c33c3793ffaa2f4c98c22790d7b587aa30c3df4fdd65143a8a2a50d523
                +------------------+--------------------------------------------------------------------+
                | Field            | Value                                                              |
                +------------------+--------------------------------------------------------------------+
                | hash             | 0xf357f2c33c3793ffaa2f4c98c22790d7b587aa30c3df4fdd65143a8a2a50d523 |
                | nonce            | 1                                                                  |
                | blockHash        | 0x07df29f220a31c43cd2792a2effa3a1187eb6c66d71a6f2cbbff29c60c3270f6 |
                | blockNumber      | 2                                                                  |
                | transactionIndex | 0                                                                  |
                | from             | 0xBe50e2b648e9A0e7E1e2B1b517C53cDAB6424355                         |
                | to               | 0x3b4720e34496A6b2357045Bf129a40bCaC87B6e1                         |
                | value            | 500000000000000000                                                 |
                | gas              | 2000000                                                            |
                | gasPrice         | 50000000000                                                        |
                | input            | 0x                                                                 |
                | v                | 27                                                                 |
                | r                | 0x4b5a13f54f054ab12cd3f2b38c3d8b8de9cfc3cb7b431e7270135f00f7402510 |
                | s                | 0x5dd02463f52bced1b990d1fc213e06930597a3fc5ef0e6b29156efe634a33748 |
                +------------------+--------------------------------------------------------------------+

            """)  # noqa
        return parser

    def take_action(self, parsed_args):
        self.log.debug('[+] showing Ethereum transaction')
        tx = parsed_args.tx[0]
        try:
            eth_tx = self.app.w3.eth.get_transaction(tx)
        except KeyError:
            sys.exit(f"[-] transaction (tx) with id '{tx}' not found")
        columns = []
        data = []
        for k, v in eth_tx.items():
            if (
                not len(parsed_args.field)
                or k in parsed_args.field
            ):
                columns.append(k)
                data.append((to_str(v)))
        return (columns, data)


# vim: set ts=4 sw=4 tw=0 et :
