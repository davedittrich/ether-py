# -*- coding: utf-8 -*-

import argparse
import logging
import textwrap

from cliff.lister import Lister
from web3 import Web3


class AccountShow(Lister):
    """Show Ethereum accounts"""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.formatter_class = argparse.RawDescriptionHelpFormatter
        parser.add_argument(
            'address',
            metavar="ADDRESS",
            nargs='?',
            default=[],
            help="Ethereum account address",
        )
        parser.epilog = textwrap.dedent("""\
            Shows Ethereum accounts.

            ::

                $ ether-py account show
                +--------------------------------------------+-------------+
                | address                                    | eth_balance |
                +--------------------------------------------+-------------+
                | 0xBe50e2b648e9A0e7E1e2B1b517C53cDAB6424355 | 100.00      |
                | 0x7eF9F0e59FC3AdD2f033cbAb86a32fC70816ED2A | 100.00      |
                | 0xC587C57EFEe451e033D853F129f7B5e61a5937C5 | 100.00      |
                | 0x4D011a188252608A15Bfb2d014f3B085ed984477 | 100.00      |
                | 0x45E1D288e47B4a39dfe6952C36fe397788Ee0417 | 100.00      |
                | 0x3b4720e34496A6b2357045Bf129a40bCaC87B6e1 | 100.00      |
                | 0x8159761d6510Aad0cA13774266914f105eFA1b9d | 100.00      |
                | 0xeA0437634B7F3699043798375281E8Cbcc5AA548 | 100.00      |
                | 0x712cF9f5a9d5F61a6aa243285be62A39Ee619ee3 | 100.00      |
                | 0xCcB9cd9A47c7688DFb6D42454Cbd3Ad748D5FDf8 | 100.00      |
                +--------------------------------------------+-------------+

                $ ether-py account show 0xC587C57EFEe451e033D853F129f7B5e61a5937C5
                +--------------------------------------------+-------------+
                | address                                    | eth_balance |
                +--------------------------------------------+-------------+
                | 0xC587C57EFEe451e033D853F129f7B5e61a5937C5 | 100.00      |
                +--------------------------------------------+-------------+

            """)  # noqa
        return parser

    def eth_balance(self, address):
        """Return the balance in ether to two decimal places."""
        balance_in_wei = self.app.w3.eth.get_balance(address)
        return f"{Web3.fromWei(balance_in_wei, 'ether'):.2f}"

    def take_action(self, parsed_args):
        self.log.debug('[+] showing Ethereum accounts')
        addresses = [a for a in self.app.w3.eth.accounts]
        columns = ['address', 'eth_balance']
        data = [
            (a, self.eth_balance(a))
            for a in addresses
            if not len(parsed_args.address) or a in parsed_args.address
        ]
        return (columns, data)

        # big_acct = '0x23735750a6ed0119e778d9bb969137df8cc8c3d1'
        # balance = contract.functions.balanceOf(
        #     w3.toChecksumAddress(big_acct)).call()
        # print(f"[+] balance of {big_acct} is "
        #       f"{w3.fromWei(balance, 'ether')}")

# vim: set ts=4 sw=4 tw=0 et :
