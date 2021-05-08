# -*- coding: utf-8 -*-

# https://solcx.readthedocs.io/en/latest/toctree.html

import os
import solcx


SOLCX_BINARY_PATH = solcx.get_solcx_install_folder(
    solcx_binary_path=os.getenv('SOLCX_BINARY_PATH', None)
)


def get_solc_versions(solcx_binary_path=SOLCX_BINARY_PATH):
    """Return solc version numbers from solcx directory."""
    return [
        fname[6:]
        for fname in os.listdir(solcx_binary_path)
        if fname.startswith('solc-v')
    ]


# vim: set ts=4 sw=4 tw=0 et :
