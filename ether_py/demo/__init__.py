# -*- coding: utf-8 -*-

import os
import sys

from ether_py import ETHERPY_CONTRACTS_DIR

VALID_CONTRACT_TYPES = [
    'abi',
    'address',
    'bytecode',
    'sol',
]


def _get_abs_path(
    file_name,
    file_ext,
    dir_path=ETHERPY_CONTRACTS_DIR
):
    """Return file name with extension from name."""
    if file_ext not in VALID_CONTRACT_TYPES:
        sys.exit(f"[-] contract file type '{file_ext}' is not valid")
    abs_path = os.path.abspath(
        os.path.join(
            dir_path,
            f"{file_name}.{file_ext}"
        )
    )
    return abs_path


def contract_filename(contract_name, file_type):
    """Return the source file path for a contract by name."""
    return _get_abs_path(contract_name, file_type)


def get_contract_data(contract_name, file_type):
    """Return the data for a named contract by type."""
    abs_path = _get_abs_path(contract_name, file_type)
    # if must_exist and not os.path.exists(abs_path):
    #     sys.exit(
    #         f"[-] file '{abs_path}' does not exist")
    with open(abs_path, 'r') as f_in:
        content = f_in.read()
    return content


def save_contract_data(contract_name, file_type, data=''):
    """Save contract related content to file."""
    abs_path = _get_abs_path(contract_name, file_type)
    with open(abs_path, 'w') as f_out:
        f_out.write(data)


# vim: set ts=4 sw=4 tw=0 et :
