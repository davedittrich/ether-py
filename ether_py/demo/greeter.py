# -*- encoding: utf-8 -*-

"""Greeter smart contract demo."""

import argparse
import json  # noqa
import logging
import os
import secrets  # noqa
import solcx
import textwrap

from cliff.command import Command
# from web3 import Web3
from ether_py import ETHERPY_CONTRACTS_DIR
from . import (
    contract_filename,
    get_contract_data,
    save_contract_data,
)


class GreeterCompile(Command):
    """Compile Greeter."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.formatter_class = argparse.RawDescriptionHelpFormatter
        parser.epilog = textwrap.dedent("""\
            Compile Greeter contract.
           \n""")
        return parser

    def take_action(self, parsed_args):
        self.log.debug('[+] demo compile Greeter contract')
        contract_name = 'Greeter'
        source_path = contract_filename(contract_name, 'sol')
        source_name = os.path.basename(source_path)
        openzeppelin = os.path.join(
            os.path.dirname(ETHERPY_CONTRACTS_DIR),
            "node_modules",
            "@openzeppelin/"
        )
        os.environ['SOLC_ARGS'] = f"openzeppelin={openzeppelin}"
        compiled_sol = solcx.compile_standard(
            {
                "language": "Solidity",
                "sources": {
                    source_name: {
                        "content": f"{get_contract_data(contract_name, 'sol')}"
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
        self.log.info(f"[+] created {contract_filename(contract_name, 'bytecode')}")  # noqa
        metadata = json.loads(compiled_sol['contracts'][source_name][contract_name]['metadata'])
        abi = metadata['output']['abi']
        save_contract_data(contract_name, 'abi', json.dumps(abi))
        self.log.info(f"[+] created {contract_filename(contract_name, 'abi')}")

    # # Get latest N blocks
    # latest_block = w3.eth.block_number
    # n = 10
    # last_n_blocks = [
    #     w3.eth.getBlock(block)
    #     for block in range(latest_block, latest_block - n, -1)
    # ]
    # # Get transaction from block by hash
    # hash = w3.toHex(last_n_blocks[0]['hash'])
    # transactions = [
    # ]
    # transaction = w3.eth.getTransactionByBlock(hash, 2)
    # pass


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
        tx_hash = w3.eth.contract(abi=abi,
                                  bytecode=bytecode).constructor().transact()
        tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        contract_address = tx_receipt.contractAddress
        save_contract_data(contract_name, 'address', contract_address)
        if self.app_args.verbose_level == 1:
            print(contract_address)
        elif self.app_args.verbose_level > 1:
            print(f"[+] transaction {contract_address} received")
        print(f"[+] greeter says '{contract.functions.greet().call()}'")


class GreeterCall(Command):
    """Call Greeter contract."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.formatter_class = argparse.RawDescriptionHelpFormatter
        # parser.add_argument(
        #     'address',
        #     nargs=1,
        #     default=None)
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
