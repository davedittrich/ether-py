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
from ether_py.utils import (
    ETHERPY_CONTRACTS_DIR,
    contract_filename,
    get_contract_data,
    save_contract_data,
    tx_receipt_to_text,
)
from solcx.exceptions import SolcNotInstalled


class GreeterCompile(Command):
    """Compile ``Greeter`` contract"""

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
            Compile the ``Greeter`` contract.

            If no compatible compiler is installed, you will get a message showing
            the pragma specified in the ``.sol`` file:

            ::

                $ ether-py demo greeter compile
                [-] No compatible solc version installed matching 'pragma solidity >=0.6.0 <0.8.0;': see 'ether-py solc install --help'

            Identify a compatible version using ``ether-py solc versions --installable``
            and install before trying again:

            ::

                $ ether-py solc install  0.7.6
                solcx                     INFO     Downloading from https://solc-bin.ethereum.org/macosx-amd64/solc-macosx-amd64-v0.7.6+commit.7338295f
                solcx                     INFO     solc 0.7.6 successfully installed at: /Users/dittrich/.solcx/solc-v0.7.6
                [+] installed solc version '0.7.6'
                $ ether-py demo greeter compile -v
                initialize_app
                [+] command line: ether-py demo greeter compile -v
                [+] established connection to ganache endpoint at http://127.0.0.1:7545
                solcx                     INFO     Using solc version 0.7.6
                [+] created /Users/dittrich/git/ether-py/contracts/Greeter.bytecode
                [+] created /Users/dittrich/git/ether-py/contracts/Greeter.abi


           \n""")  # noqa
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
    """Load ``Greeter`` contract"""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.formatter_class = argparse.RawDescriptionHelpFormatter
        parser.epilog = textwrap.dedent("""\
            Saves the ``Greeter`` contract to the ethereum blockchain.

            ::

                $ ether-py demo -v greeter load
                initialize_app
                [+] command line: ether-py demo -v greeter load
                [+] established connection to ganache endpoint at http://127.0.0.1:7545
                [+] transaction 0xF43Dd5d4f35D468c65B96901B93e8BCaD6F3C210 received
                [+] greeter says 'Hello'

           \n""")  # noqa
        return parser

    def take_action(self, parsed_args):
        self.log.debug('[+] load Greeter contract')
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
        tx_receipt_text = tx_receipt_to_text(tx_receipt)
        save_contract_data(contract_name, 'receipt', tx_receipt_text)
        contract_address = tx_receipt.contractAddress
        save_contract_data(contract_name, 'address', contract_address)
        if self.app_args.verbose_level == 1:
            print(contract_address)
        elif self.app_args.verbose_level > 1:
            print(f"[+] transaction {contract_address} received")
        if self.app_args.verbose_level > 2:
            for line in tx_receipt_text.split('\n'):
                print(f"[+] {line}")
        if self.app_args.verbose_level == 1:
            contract = w3.eth.contract(address=contract_address, abi=abi)
            print(f"[+] greeter says '{contract.functions.greet().call()}'")


class GreeterCall(Command):
    """Call ``Greeter`` contract"""

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
