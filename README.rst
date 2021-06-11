.. ether_py documentation master file, created by
   cookiecutter on 2021-03-29.

ether-py
========

|Versions| |Contributors| |License| |Docs|

.. |Versions| image:: https://img.shields.io/pypi/pyversions/ether-py.svg
   :target: https://pypi.org/project/ether-py
.. |Contributors| image:: https://img.shields.io/github/contributors/davedittrich/ether-py.svg
   :target: https://github.com/davedittrich/ether-py/graphs/contributors
.. |License| image:: https://img.shields.io/github/license/davedittrich/ether-py.svg
   :target: https://github.com/davedittrich/ether-py/blob/master/LICENSE
.. |Docs| image:: https://readthedocs.org/projects/ether-py/badge/?version=latest
   :target: https://ether-py.readthedocs.io

``ether-py`` provides a general Python command line interface (CLI) for interacting with
the Ethereum blockchain.


* Version: 2021.3.0
* GitHub repo: https://github.com/davedittrich/ether-py/
* License: Apache Software License 2.0


.. README_FEATURES

Features
--------

* ``ether-py`` provides a general Python command line interface (CLI)
  built on the OpenStack
  `cliff -- Command Line Interface Formulation Framework <https://github.com/openstack/cliff>`_.
* ``cliff`` provides many useful features like modularizing subcommands into
  groups, built-in help for internally documenting commands, and producing
  output in clean tabular form or in one of several data formats you can
  feed into other tools or automation platforms.
* `Sphinx <http://www.sphinx-doc.org/>`_ documentation for generation with `ReadTheDocs <https://readthedocs.com>`_
  including ``cliff`` autoprogram `Sphinx integration <https://docs.openstack.org/cliff/latest/user/sphinxext.html>`_
  for documenting commands from the same ``--help`` output you can get at the command line.
* Uses the `python_secrets <https://pypi.org/project/python-secrets>`_ package (``psec``)
  to manage endpoint configuration settings and access control tokens to prevent secrets
  leakage and to make it easy to switch between local development/testing using
  `ganache <https://www.trufflesuite.com/ganache>`_ and accessing a
  live Ethereum blockchain using `Infura endpoints <https://infura.io>`_.
* Uses `py-solc-x <https://github.com/iamdefinitelyahuman/py-solc-x>`_ for installing Solidity
  compilers and compiling Solidity smart contracts (``.sol`` files)
  `dependabot <https://docs.github.com/en/code-security/supply-chain-security/configuring-dependabot-security-updates>`_.


Contact
-------

Dave Dittrich <dave.dittrich@gmail.com>

.. |copy|   unicode:: U+000A9 .. COPYRIGHT SIGN

Copyright |copy| 2021 Dave Dittrich. All rights reserved.

Credits
-------

This package was created with `Cookiecutter
<https://github.com/cookiecutter/cookiecutter>`_ from the
<https://github.com/davedittrich/cookiecutter-cliffapp-template> project template.  It
derives some of its features and inspiration from
<https://github.com/veit/cookiecutter-namespace-template> and
<https://github.com/audreyfeldroy/cookiecutter-pypackage>.


.. EOF
