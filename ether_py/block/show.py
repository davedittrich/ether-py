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

            ::

                $ ether-py block show latest --fit-width
                +------------------+-------------------------------------------------------------------------------------------------------------------------+
                | Field            | Value                                                                                                                   |
                +------------------+-------------------------------------------------------------------------------------------------------------------------+
                | number           | 15                                                                                                                      |
                | hash             | 0x008547e530fe0965d3711d25fbb1d20264c16d525f02aa280633c1a721ff5720                                                      |
                | parentHash       | 0xc95783fb95338588b8bffe4c88eb979086e0c6b6fdd1a78bc591319c3270906d                                                      |
                | mixHash          | 0x0000000000000000000000000000000000000000000000000000000000000000                                                      |
                | nonce            | 0x0000000000000000                                                                                                      |
                | sha3Uncles       | 0x1dcc4de8dec75d7aab85b567b6ccd41ad312451b948a7413f0a142fd40d49347                                                      |
                | logsBloom        | 0x000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000 |
                |                  | 00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000 |
                |                  | 00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000 |
                |                  | 00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000 |
                |                  | 00000000000000000000000000000000000000                                                                                  |
                | transactionsRoot | 0x9f619679ac0f15e5725d63c06bf352f88a2eb002d7bbb983188a929c10f38de1                                                      |
                | stateRoot        | 0xeb0ae3b8c7beb461793f9780d4e180515843f60227768c3b19b0472216673ed6                                                      |
                | receiptsRoot     | 0xd5420f0d6143865fa94e3464abb47a054c4f83dd5b9159603616fe39b97dd2b2                                                      |
                | miner            | 0x0000000000000000000000000000000000000000                                                                              |
                | difficulty       | 0                                                                                                                       |
                | totalDifficulty  | 0                                                                                                                       |
                | extraData        | 0x                                                                                                                      |
                | size             | 1000                                                                                                                    |
                | gasLimit         | 6721975                                                                                                                 |
                | gasUsed          | 313249                                                                                                                  |
                | timestamp        | 1618011641                                                                                                              |
                | transactions     | [HexBytes('0x07a137a05974311c877874d5fd699d90adfeb4fca10c95d989285a504af39b2d')]                                        |
                | uncles           | []                                                                                                                      |
                +------------------+-------------------------------------------------------------------------------------------------------------------------+

            ..""")
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
