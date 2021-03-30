# -*- coding: utf-8 -*-

import datetime
import os
import textwrap

ETHERPY_DATA_DIR = os.environ.get(
    "ETHERPY_DATA_DIR",
    os.getcwd()
)


def copyright():
    """Copyright string"""
    this_year = str(datetime.datetime.today().year)
    copyright_years = (
        f'2021-{this_year}'
        if '2021' != this_year
        else '2021'
    )
    copyright = textwrap.dedent(f"""
        This program was bootstrapped from a ``cookiecutter`` template created
        by Dave Dittrich <dave.dittrich@gmail.com>:

            https://github.com/davedittrich/cookiecutter-cliffapp-template.git
            https://cookiecutter-cliffapp-template.readthedocs.io

        Author:    Dave Dittrich <dave.dittrich@gmail.com>
        Copyright: {copyright_years}, Dave Dittrich. All rights reserved.
        License:   Apache Software License 2.0
        URL:       https://pypi.python.org/pypi/ether-py""")  # noqa
    return copyright


__author__ = 'Dave Dittrich'
__copyright__ = copyright()
__email__ = 'dave.dittrich@gmail.com'
__license__ = 'Apache Software License 2.0'
__name__ = 'ether-py'
__release__ = '2021.3.0'
__version__ = None
__summary__ = 'The ether-py Ethereum command line interface.'
__title__ = 'ether-py'
__url__ = 'https://github.com/davedittrich/ether-py'

# Get development version from repository tags?
try:
    from setuptools_scm import get_version
    __version__ = get_version(root='..', relative_to=__file__)
except (LookupError, ModuleNotFoundError):
    pass

if __version__ is None:
    from pkg_resources import get_distribution, DistributionNotFound
    try:
        __version__ = get_distribution("ether_py").version
    except (DistributionNotFound, ModuleNotFoundError):
        pass

if __version__ is None:
    __version__ = __release__


__all__ = [
    '__author__',
    '__copyright__',
    '__email__',
    '__release__',
    '__summary__',
    '__title__',
    '__url__',
    '__version__',
]

# vim: set ts=4 sw=4 tw=0 et :
