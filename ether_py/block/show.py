# -*- coding: utf-8 -*-

import argparse
import logging
import textwrap
import sys

from ether_py.utils import to_str
from cliff.show import ShowOne


class BlockShow(ShowOne):
    """Show Ethereum block"""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.formatter_class = argparse.RawDescriptionHelpFormatter
        parser.add_argument(
            'block',
            metavar='BLOCK',
            nargs=1,
            default=None,
            help="Ethereum block number",
        )
        parser.add_argument(
            'field',
            metavar='FIELD',
            nargs='?',
            default=[],
            help="Block metadata field",
        )
        parser.epilog = textwrap.dedent("""\
            Get an Ethereum block.

            The block number should be the block's number, its hash,
            or the word "latest" to get the most recent block.
            """)
        return parser

    def take_action(self, parsed_args):
        self.log.debug('[+] showing Ethereum block')
        block = parsed_args.block[0]
        try:
            eth_block = self.app.w3.eth.get_block(block)
        except KeyError:
            sys.exit(f"[-] block with id '{block}' not found")
        columns = []
        data = []
        fields = [f.lower() for f in parsed_args.field]
        for k, v in eth_block.items():
            if not len(fields) or k.lower() in fields:
                columns.append(k)
                data.append((to_str(v)))
        return (columns, data)


# vim: set ts=4 sw=4 tw=0 et :
