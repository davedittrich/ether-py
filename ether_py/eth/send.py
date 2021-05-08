# -*- coding: utf-8 -*-

import argparse
import logging
import secrets
import textwrap

from cliff.command import Command


class EthSend(Command):
    """Send Ethereum"""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.formatter_class = argparse.RawDescriptionHelpFormatter
        # parser.add_argument(
        #     'from',
        #     metavar='FROM',
        #     nargs=1,
        #     default=None,
        #     help="Sending account",
        # )
        # parser.add_argument(
        #     'to',
        #     metavar='TO',
        #     nargs=1,
        #     default=None,
        #     help="Receiving account",
        # )
        parser.add_argument(
            'eth',
            metavar='ETH',
            nargs=1,
            default=None,
            help="Transaction amount in eth",
        )
        parser.epilog = textwrap.dedent("""\
            Send Ethereum from one address to another.
            ::

                $ ether_py eth send FROM TO ETH
            """)
        return parser

    def take_action(self, parsed_args):
        self.log.debug('[+] sending Ethereum')
        w3 = self.app.w3
        from_account_address = '0xBe50e2b648e9A0e7E1e2B1b517C53cDAB6424355'
        from_account_key = 'c931988d78b75bd3add16e52e432603e7a762f6364d7d780355d8f0955cda364'  # noqa
        accounts = w3.eth.get_accounts()
        # Randomly chose one account (other than the chosen from account).
        to_account_address = next(
            account for account in secrets.SystemRandom().sample(accounts, 2)
            if account != from_account_address
        )
        nonce = w3.eth.getTransactionCount(from_account_address)
        tx = {
            'nonce': nonce,
            'to': to_account_address,
            'value': w3.toWei(float(parsed_args.eth[0]), 'ether'),
            'gas': 2000000,
            'gasPrice': w3.toWei('50', 'gwei')
        }
        signed_tx = w3.eth.account.signTransaction(tx, from_account_key)
        tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
        if self.app_args.verbose_level == 1:
            print(w3.toHex(tx_hash))
        elif self.app_args.verbose_level > 1:
            print(f"[+] transaction {w3.toHex(tx_hash)} sent")


# vim: set ts=4 sw=4 tw=0 et :
