# -*- coding: utf-8 -*-

import argparse
import logging
import textwrap
import sys

from cliff.command import Command


class BlockGet(Command):
    """Get Ethereum block"""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.formatter_class = argparse.RawDescriptionHelpFormatter
        parser.add_argument(
            'block',
            nargs=1,
            default=None)
        parser.epilog = textwrap.dedent("""\
            Get an Ethereum block.

            The block number should be the block's number, its hash,
            or the word "latest" to get the most recent block.
            """)
        return parser

    def take_action(self, parsed_args):
        self.log.debug('[+] getting Ethereum block')
        block = parsed_args.block[0]
        if not (type(block) is int or block == 'latest'):
            sys.exit(f"[-] '{block}' is not a valid block")
        eth_block = self.app.w3.eth.get_block(block)  # noqa
        raise RuntimeError('[!] NOT IMPLEMENTED')

# vim: set ts=4 sw=4 tw=0 et :
