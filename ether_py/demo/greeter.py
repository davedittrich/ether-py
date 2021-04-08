# -*- encoding: utf-8 -*-

"""Greeter smart contract demo."""

import argparse
import json  # noqa
import logging
import os
import secrets  # noqa
import solcx
import sys
import textwrap

from cliff.command import Command
# from web3 import Web3
from ether_py import ETHERPY_CONTRACTS_DIR
from . import (
    contract_filename,
    get_contract_data,
    save_contract_data,
)
from solcx.exceptions import SolcNotInstalled


class GreeterCompile(Command):
    """Compile Greeter."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.formatter_class = argparse.RawDescriptionHelpFormatter
        parser.add_argument(
            '--solc-version',
            dest='solc_version',
            default="latest",
            help="Use solc compiler version (default: 'latest')"
        )
        parser.epilog = textwrap.dedent("""\
            Compile Greeter contract.
           \n""")
        return parser

    def take_action(self, parsed_args):
        self.log.debug('[+] demo compile Greeter contract')
        contract_name = 'Greeter'
        source_path = contract_filename(contract_name, 'sol')
        source_sol = get_contract_data(contract_name, 'sol')
        source_name = os.path.basename(source_path)
        openzeppelin = os.path.join(
            os.path.dirname(ETHERPY_CONTRACTS_DIR),
            "node_modules",
            "@openzeppelin/"
        )
        version_pragma = None
        if parsed_args.solc_version is None:
            version_pragma = f"pragma solidity ^{parsed_args.solc_version};"
        else:
            for line in source_sol.split('\n'):
                if line.startswith('pragma solidity'):
                    version_pragma = line
                    break
        os.environ['SOLC_ARGS'] = f"openzeppelin={openzeppelin}"
        try:
            solcx.set_solc_version_pragma(version_pragma)
        except SolcNotInstalled as err:
            sys.exit(
                f"[-] {err.args[0].split('.')[0]} matching "
                f"'{version_pragma}': see 'ether-py solc install --help'"
            )
        compiled_sol = solcx.compile_standard(
            {
                "language": "Solidity",
                "sources": {
                    source_name: {
                        "content": f"{source_sol}"
                    }
                },
                "settings": {
                    "outputSelection": {
                        "*": {
                            "*": [
                                "metadata",
                                "evm.bytecode",
                                "evm.bytecode.sourceMap"
                            ]
                        }
                    }
                }
            },
            allow_paths=openzeppelin,
        )
        bytecode = compiled_sol['contracts'][source_name][contract_name]['evm']['bytecode']['object']  # noqa
        save_contract_data(contract_name, 'bytecode', bytecode)
        print(f"[+] created {contract_filename(contract_name, 'bytecode')}")  # noqa
        metadata = json.loads(compiled_sol['contracts'][source_name][contract_name]['metadata'])  # noqa
        abi = metadata['output']['abi']
        save_contract_data(contract_name, 'abi', json.dumps(abi))
        print(f"[+] created {contract_filename(contract_name, 'abi')}")


class GreeterLoad(Command):
    """Load Greeter contract."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.formatter_class = argparse.RawDescriptionHelpFormatter
        parser.epilog = textwrap.dedent("""\
            FILL THIS IN.
           \n""")
        return parser

    def take_action(self, parsed_args):
        self.log.debug('[+] demo load Greeter contract')
        w3 = self.app.w3
        contract_name = 'Greeter'
        # Set default account for transaction
        w3.eth.default_account = w3.eth.accounts[0]
        bytecode = get_contract_data(contract_name, 'bytecode')
        abi = json.loads(get_contract_data(contract_name, 'abi'))
        tx_hash = w3.eth.contract(
            abi=abi,
            bytecode=bytecode).constructor().transact()
        tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        contract_address = tx_receipt.contractAddress
        save_contract_data(contract_name, 'address', contract_address)
        if self.app_args.verbose_level == 1:
            print(contract_address)
        elif self.app_args.verbose_level > 1:
            print(f"[+] transaction {contract_address} received")
            contract = w3.eth.contract(address=contract_address, abi=abi)
            print(f"[+] greeter says '{contract.functions.greet().call()}'")


class GreeterCall(Command):
    """Call Greeter contract."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.formatter_class = argparse.RawDescriptionHelpFormatter
        parser.add_argument(
            'message',
            nargs=1,
            default=None)
        parser.epilog = textwrap.dedent("""\
            Call the Greeter contract with a message.
           \n""")
        return parser

    def take_action(self, parsed_args):
        self.log.debug('[+] call Greeter contract')
        w3 = self.app.w3
        # Set default account for transaction
        w3.eth.default_account = w3.eth.accounts[0]
        address = get_contract_data('Greeter', 'address')
        abi = json.loads(get_contract_data('Greeter', 'abi'))
        contract = w3.eth.contract(address=address, abi=abi)
        message = parsed_args.message[0]
        greeting = contract.functions.greet().call()
        print(f"[+] greet() returns '{greeting}'")
        if greeting != message:
            print(f"[+] calling setGreeting({message})")
            tx_hash = contract.functions.setGreeting(message).transact()
            tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
            print(f"[+] greeter now says '{contract.functions.greet().call()}'")
            if self.app_args.verbose_level == 1:
                print(w3.toHex(tx_receipt.transactionHash))
            elif self.app_args.verbose_level > 1:
                print("[+] transaction "
                      f"{w3.toHex(tx_receipt.transactionHash)} received")
                print(f"[+] used {tx_receipt.gasUsed} gas "
                      f"(cumulatively {tx_receipt.cumulativeGasUsed}")


# vim: set ts=4 sw=4 tw=0 et :
