# -*- encoding: utf-8 -*-

"""The ether-py Ethereum command line interface."""

# See the COPYRIGHT variable in ether_py/__init__.py (also found
# in output of ``ether-py help``).

# Standard library modules.
import argparse
import coloredlogs
import logging
import os
import sys
import textwrap

from . import (
    __version__,
    ETHERPY_DATA_DIR,
)
from ether_py.utils import (
    ganache_url,
    infura_url,
    Timer,
)
# External dependencies.

from cliff.app import App
from cliff.commandmanager import CommandManager
from psec.secrets import SecretsEnvironment
from web3 import Web3


if sys.version_info < (3, 6, 0):
    print(f"The { os.path.basename(sys.argv[0]) } program "
          "prequires Python 3.6.0 or newer\n"
          "Found Python { sys.version }", file=sys.stderr)
    sys.exit(1)


def default_environment(default='ether-py'):
    """Return environment identifier"""
    return os.getenv('ETHERPY', default)


class Ether_pyApp(App):
    """The ether-py Ethereum command line interface."""

    def __init__(self):
        super().__init__(
            description=__doc__.strip(),
            version=__version__,
            command_manager=CommandManager(
                namespace='ether_py'
            ),
            deferred_help=True,
        )
        self.environment = None
        self.se = None
        self.timer = Timer()

    def build_option_parser(self, description, version):
        parser = super().build_option_parser(
            description,
            version
        )
        parser.formatter_class = argparse.RawDescriptionHelpFormatter
        # Global options
        parser.add_argument(
            '-D', '--data-dir',
            metavar='<data-directory>',
            dest='data_dir',
            default=ETHERPY_DATA_DIR,
            help=('Root directory for holding data files '
                  f"(Env: ``ETHERPY_DATA_DIR``; "
                  f"default: { ETHERPY_DATA_DIR })")
        )
        parser.add_argument(
            '-e', '--elapsed',
            action='store_true',
            dest='elapsed',
            default=False,
            help=('Include elapsed time (and ASCII bell) '
                  'on exit (default: False)')
        )
        parser.add_argument(
            '-E', '--environment',
            metavar='<environment>',
            dest='environment',
            default=default_environment(),
            help=('Deployment environment selector '
                  "(Env: ``ETHERPY_ENVIRONMENT``; "
                  f'default: {default_environment()})')
        )
        from ether_py import copyright
        parser.epilog = textwrap.dedent(f"""
        For help information on individual commands, use ``ether-py <command> --help``.

        Several commands have features that will attempt to open a browser. See
        ``ether-py about --help`` to see help information about this feature and how
        to control which browser(s) will be used.

        { copyright() }""")  # noqa
        return parser

    def setup_logging(self, log_level=logging.DEBUG):
        """Setup root logger and quiet some levels."""
        # Credit: https://web3py.readthedocs.io/en/latest/examples.html#contract-unit-tests-in-python  # noqa

        # Set log format to dislay the logger name
        # to hunt down verbose logging modules
        fmt = "%(name)-25s %(levelname)-8s %(message)s"

        # Use colored logging output for console with the coloredlogs package
        # https://pypi.org/project/coloredlogs/
        coloredlogs.install(level=log_level, fmt=fmt, logger=self.LOG)

        # Disable logging of JSON-RPC requests and replies
        logging.getLogger("web3.RequestManager").setLevel(logging.WARNING)
        logging.getLogger("web3.providers.HTTPProvider").setLevel(logging.WARNING)  # noqa
        # logging.getLogger("web3.RequestManager").propagate = False

        # Disable all internal debug logging of requests and urllib3
        # E.g. HTTP traffic
        logging.getLogger("requests").setLevel(logging.WARNING)
        logging.getLogger("urllib3").setLevel(logging.WARNING)

    def setup_endpoint(self):
        """Establish connection with Ethereum network endpoint."""
        self.infura_project_id = self.se.get_secret('infura_project_id')
        self.infura_endpoint = self.se.get_secret('infura_endpoint')
        self.infura_api_version = self.se.get_secret('infura_api_version')
        self.ethereum_address = self.se.get_secret('ethereum_address')
        if self.infura_endpoint == 'ganache':
            # Ganache test server is treated like Infura endpoint.
            self.ethereum_host = self.se.get_secret('ganache_host')
            self.ethereum_port = self.se.get_secret('ganache_port')
            self.ethereum_url = ganache_url(host=self.ethereum_host,
                                            port=self.ethereum_port)
        else:
            self.ethereum_url = infura_url(
                endpoint=self.infura_endpoint,
                project_id=self.infura_project_id,
                api_version=self.infura_api_version)
        self.w3 = Web3(Web3.HTTPProvider(self.ethereum_url))
        if not self.w3.isConnected():
            sys.exit(f'[+] connection to {self.ethereum_url} failed')
        if self.options.verbose_level > 1 or self.options.debug:
            self.LOG.info(f'[+] established connection to {self.ethereum_url}')
        self.LOG.debug(f'[+] api {self.w3.api}, '
                       f'clientVersion {self.w3.clientVersion}')
        # self.LOG.info('[+] current ethereum block is '
        #               f'{self.w3.eth.blockNumber}')
        # self.ethereum_balance = self.w3.fromWei(
        #     self.w3.eth.getBalance(account=self.ethereum_address),
        #     'ether')
        # self.LOG.info('[+] current ether balance is '
        #               f'{self.ethereum_balance}')

    def initialize_app(self, argv):
        self.LOG.debug('initialize_app')
        self.setup_logging(
            log_level=logging.DEBUG if self.options.debug else logging.INFO)
        self.set_environment(self.options.environment)
        # Load configuration from default python-secrets environment
        # and export them environment variables for programs running
        # in child processes (e.g., Vagrant) to access.
        self.se = SecretsEnvironment(environment=self.environment,
                                     export_env_vars=True)
        self.se.read_secrets_and_descriptions()
        self.setup_endpoint()

    def prepare_to_run_command(self, cmd):
        if cmd.app_args.verbose_level > 1:
            self.LOG.info('[+] command line: {}'.format(
                " ".join([arg for arg in sys.argv])
            ))
        self.LOG.debug('prepare_to_run_command %s', cmd.__class__.__name__)
        if self.options.elapsed:
            self.timer.start()

    def clean_up(self, cmd, result, err):
        self.LOG.debug('[!] clean_up %s', cmd.__class__.__name__)
        if self.options.elapsed:
            self.timer.stop()
            elapsed = self.timer.elapsed()
            if result != 0:
                self.LOG.debug('[!] elapsed time: %s', elapsed)
            elif (
                self.options.verbose_level >= 0
                and cmd.__class__.__name__ != "CompleteCommand"
            ):
                self.stdout.write('[+] Elapsed time {}\n'.format(elapsed))
                if sys.stdout.isatty():
                    sys.stdout.write('\a')
                    sys.stdout.flush()

    def set_environment(self, environment=default_environment()):
        """Set variable for current environment"""
        self.environment = environment

    def get_environment(self):
        """Get the current environment setting"""
        return self.environment


def main(argv=sys.argv[1:]):
    """
    Command line interface for the ``ether-py`` project.
    """

    try:
        myapp = Ether_pyApp()
        result = myapp.run(argv)
    except KeyboardInterrupt:
        sys.stderr.write("\nReceived keyboard interrupt: exiting\n")
        result = 1
    return result


if __name__ == '__main__':
    # Ensure that running program with either "python -m ether_py"
    # or just "ether-py" result in same argv.
    if sys.argv[0].endswith('__main__.py'):
        sys.argv[0] = os.path.basename(os.path.dirname(sys.argv[0]))
    sys.exit(main(sys.argv[1:]))

# EOF
