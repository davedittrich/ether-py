# -*- coding: utf-8 -*-

import argparse
import logging
import os
import textwrap

from cliff.lister import Lister
from ether_py.utils import (
    ETHERPY_CONTRACTS_DIR,
    VALID_CONTRACT_TYPES,
    # contract_filename,
    # get_contract_data,
    # save_contract_data,
    # tx_receipt_to_text,
)

check_extensions = [
    t for t in VALID_CONTRACT_TYPES
    if t != 'sol'
]


def exists_file(name, ext, all_files):
    """Return 'Yes' or 'No' for file existence."""
    fullname = f"{name}.{ext}"
    return "Yes" if fullname in all_files else "No"


class ContractList(Lister):
    """List contract files"""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.formatter_class = argparse.RawDescriptionHelpFormatter
        # parser.add_argument(
        #     '--installable',
        #     action='store_true',
        #     dest='installable',
        #     default=False,
        #     help=('Show installable versions (default: False)')
        # )
        parser.add_argument(
            'name',
            nargs='?',
            default=None)
        parser.epilog = textwrap.dedent(f"""\
            List Solidity contracts and related files.

            Solidity contracts are compiled from source code in ``.sol`` files.
            By convention, ``ether-py`` expects the contact name to be the same
            as the ``.sol`` file without the extension (so ``Greeter.sol`` is
            the source file for the contract ``Greeter``).

            Only contracts with files having ``.sol`` extensions are listed. Initially,
            just those files exist and none of the related file types::

                $ ether-py contract list
                +----------------------+-----+---------+----------+---------+
                | name                 | abi | address | bytecode | receipt |
                +----------------------+-----+---------+----------+---------+
                | Greeter              | No  | No      | No       | No      |
                | SimpleCollectible    | No  | No      | No       | No      |
                +----------------------+-----+---------+----------+---------+

            As contracts are compiled and loaded, additional files with file
            extensions in the following set are created:

            {{ {', '.join([f"``.{e}``" for e in check_extensions])} }}

            After compiling the contract, the ``.abi`` and ``.bytecode`` files
            will exist::

                $ ether-py demo greeter compile
                solcx                     INFO     Using solc version 0.7.6
                [+] created /Users/dittrich/git/ether-py/contracts/Greeter.bytecode
                [+] created /Users/dittrich/git/ether-py/contracts/Greeter.abi
                $ ether-py contract list
                +----------------------+-----+---------+----------+---------+
                | name                 | abi | address | bytecode | receipt |
                +----------------------+-----+---------+----------+---------+
                | Greeter              | Yes | No      | Yes      | No      |
                | SimpleCollectible    | No  | No      | No       | No      |
                +----------------------+-----+---------+----------+---------+


            After loading the contract into the Ethereum blockchain, the
            ``.address`` and ``.receipt`` files will exist::

                $ ether-py demo greeter load
                0x22785519732f4623B9D3096bE3bCDF47053cA035
                [+] greeter says 'Hello'
                $ ether-py contract list
                +----------------------+-----+---------+----------+---------+
                | name                 | abi | address | bytecode | receipt |
                +----------------------+-----+---------+----------+---------+
                | Greeter              | Yes | Yes     | Yes      | Yes     |
                | SimpleCollectible    | No  | No      | No       | No      |
                +----------------------+-----+---------+----------+---------+

            """)  # noqa
        return parser

    def take_action(self, parsed_args):
        self.log.debug('[+] listing contract related files')
        # We're only going to show existence of files other
        # than .sol files. They are implicit.

        columns = ['name'] + check_extensions
        contract_names = [
            os.path.splitext(name)[0]
            for name in os.listdir(ETHERPY_CONTRACTS_DIR)
            if name.endswith('.sol')
        ]
        contract_names.sort()
        all_files = [
            name for name in os.listdir(ETHERPY_CONTRACTS_DIR)
            if not name.startswith('.')
            and os.path.splitext(name)[1][1:] in check_extensions
        ]
        # First column is just the name. The .sol file is implicit,
        # but other file types are listed as "Yes" or "No" depending
        # on whether they exist or not.
        data = []
        for name in contract_names:
            data.append(
                [name] + [
                    exists_file(name, ext, all_files)
                    for ext in check_extensions
                ]
            )
        return (columns, data)


# vim: set ts=4 sw=4 tw=0 et :
