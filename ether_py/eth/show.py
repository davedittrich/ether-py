# -*- coding: utf-8 -*-

import argparse
import logging
import textwrap

from ether_py.utils import to_str
from cliff.show import ShowOne


class EthShow(ShowOne):
    """Show Ethereum blockchain information."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.formatter_class = argparse.RawDescriptionHelpFormatter
        parser.add_argument(
            'field',
            nargs='?',
            default=[])
        parser.epilog = textwrap.dedent("""\
            Shows attributes about Ethereum blockchain.

            ::

                $ ether_py eth show
            """)
        return parser

    def take_action(self, parsed_args):
        self.log.debug('[+] showing Ethereum blockchain info')
        columns = []
        data = []
        fields = [f.lower() for f in parsed_args.field]
        net_attributes = ['is_async', 'listening', 'peer_count', 'version']
        for k in net_attributes:
            if not len(fields) or k.lower() in fields:
                columns.append(k)
                data.append((to_str(getattr(self.app.w3.net, k))))
        return (columns, data)


# vim: set ts=4 sw=4 tw=0 et :
