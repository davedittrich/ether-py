# -*- coding: utf-8 -*-

import logging
import os
import sys
import time
import webbrowser

from collections import OrderedDict
from ether_py import ETHERPY_CONTRACTS_DIR
from web3 import Web3
from web3.types import (
    HexBytes
)


BROWSER = os.getenv('BROWSER', None)
INFURA_TLD = 'infura.io'
# Use syslog for logging?
# TODO(dittrich): Make this configurable, since it can fail on Mac OS X
SYSLOG = False
TX_ATTRIBUTES = {
    'blockHash': Web3.toHex,
    'blockNumber': int,
    'contractAddress': str,
    'cumulativeGasUsed': int,
    'from': str,
    'gasUsed': int,
    'logs': str,
    'logsBloom': Web3.toHex,
    'status': int,
    'to': str,
    'transactionHash': Web3.toHex,
    'transactionIndex': int,
}
VALID_CONTRACT_TYPES = [
    'abi',
    'address',
    'bytecode',
    'sol',
    'receipt',
]


logger = logging.getLogger(__name__)


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
    with open(abs_path, 'r') as f_in:
        content = f_in.read()
    return content


def save_contract_data(contract_name, file_type, data=''):
    """Save contract related content to file."""
    abs_path = _get_abs_path(contract_name, file_type)
    with open(abs_path, 'w') as f_out:
        f_out.write(data)


def tx_receipt_to_text(tx_receipt):
    """Convert a transaction receipt to text form."""
    return "\n".join(
        [
            f"{item}: {to_str(getattr(tx_receipt, item))}"
            for item in TX_ATTRIBUTES.keys()
        ]
    )


def ganache_url(host='127.0.0.1', port='7445'):
    """Return URL for Ganache test server."""
    return f"http://{host}:{port}"


def infura_url(
    endpoint='mainnet',
    project_id=None,
    api_version='v3'
):
    """Return full project URL for Infura endpoint."""
    return f"https://{endpoint}.{INFURA_TLD}/{api_version}/{project_id}"


def to_str(item):
    if type(item) is HexBytes:
        return Web3.toHex(item)
    # elif type(item) is list:
    #     return str(item)
    else:
        return str(item)


def elapsed(start, end):
    assert isinstance(start, float)
    assert isinstance(end, float)
    assert start >= 0.0
    assert start <= end
    hours, rem = divmod(end - start, 3600)
    minutes, seconds = divmod(rem, 60)
    return (f"{int(hours):0>2}:"
            f"{int(minutes):0>2}:"
            f"{seconds:05.2f}")


# TODO(dittrich): Import from psec (once circular import issue fixed)
class Timer(object):
    """
    Timer object usable as a context manager, or for manual timing.
    Based on code from http://coreygoldberg.blogspot.com/2012/06/python-timer-class-context-manager-for.html  # noqa

    As a context manager, do:

        from timer import Timer

        url = 'https://github.com/timeline.json'

        with Timer() as t:
            r = requests.get(url)

        print 'fetched %r in %.2f msec' % (url, t.elapsed*1000)

    """

    def __init__(self, task_description='elapsed time', verbose=False):
        self.verbose = verbose
        self.task_description = task_description
        self.laps = OrderedDict()

    def __enter__(self):
        """Record initial time."""
        self.start(lap="__enter__")
        if self.verbose:
            sys.stdout.write(f'{self.task_description}...')
            sys.stdout.flush()
        return self

    def __exit__(self, *args):
        """Record final time."""
        self.stop()
        backspace = '\b\b\b'
        if self.verbose:
            sys.stdout.flush()
            if self.elapsed_raw() < 1.0:
                sys.stdout.write(backspace + ':' + '{:.2f}ms\n'.format(
                    self.elapsed_raw() * 1000))
            else:
                sys.stdout.write(backspace + ': ' + '{}\n'.format(
                    self.elapsed()))
            sys.stdout.flush()

    def start(self, lap=None):
        """Record starting time."""
        t = time.time()
        first = None if len(self.laps) == 0 \
            else self.laps.iteritems().next()[0]
        if first is None:
            self.laps["__enter__"] = t
        if lap is not None:
            self.laps[lap] = t
        return t

    def lap(self, lap="__lap__"):
        """
        Records a lap time.
        If no lap label is specified, a single 'last lap' counter will be
        (re)used. To keep track of more laps, provide labels yourself.
        """
        t = time.time()
        self.laps[lap] = t
        return t

    def stop(self):
        """Record stop time."""
        return self.lap(lap="__exit__")

    def get_lap(self, lap="__exit__"):
        """Get the timer for label specified by 'lap'"""
        return self.lap[lap]

    def elapsed_raw(self, start="__enter__", end="__exit__"):
        """Return the elapsed time as a raw value."""
        return self.laps[end] - self.laps[start]

    def elapsed(self, start="__enter__", end="__exit__"):
        """
        Return a formatted string with elapsed time between 'start'
        and 'end' kwargs (if specified) in HH:MM:SS.SS format.
        """
        hours, rem = divmod(self.elapsed_raw(start, end), 3600)
        minutes, seconds = divmod(rem, 60)
        return "{:0>2}:{:0>2}:{:05.2f}".format(
            int(hours), int(minutes), seconds)


def add_browser_options(parser):
    """Add web browser options."""
    parser.add_argument(
        '--browser',
        action='store',
        dest='browser',
        default=BROWSER,
        help=f'Browser to use for viewing (default: {BROWSER}).'
    )
    parser.add_argument(
        '--force',
        action='store_true',
        dest='force',
        default=False,
        help=("Open the browser even if process has no TTY "
              "(default: False)")
    )
    return parser


def open_browser(page=None, browser=None, force=False):
    """Open web browser to page."""
    if not sys.stdin.isatty() and not force:
        raise RuntimeError(
            "[-] use --force to open browser when stdin is not a TTY")
    if page is None:
        raise RuntimeError("[-] not page specified")
    which = "system default" if browser is None else browser
    logger.info(f"[+] opening browser '{which}' for {page}")
    if browser is not None:
        webbrowser.get(browser).open_new_tab(page)
    else:
        webbrowser.open(page, new=1)


# vim: set ts=4 sw=4 tw=0 et :
