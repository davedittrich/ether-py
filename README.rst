.. ether_py documentation master file, created by
   cookiecutter on 2021-03-29.

ether-py
========

|Versions| |Contributors| |License| |Docs|

.. |Versions| image:: https://img.shields.io/pypi/pyversions/ether-py.svg
   :target: https://pypi.org/project/ether-py
.. |Contributors| image:: https://img.shields.io/github/contributors/davedittrich/ether_py.svg
   :target: https://github.com/davedittrich/ether_py/graphs/contributors
.. |License| image:: https://img.shields.io/github/license/davedittrich/ether-py.svg
   :target: https://github.com/davedittrich/ether-py/blob/master/LICENSE
.. |Docs| image:: https://readthedocs.org/projects/ether-py/badge/?version=latest
   :target: https://ether-py.readthedocs.io

The ether-py Ethereum command line interface.

* Version: 2021.3.0
* GitHub repo: https://github.com/davedittrich/ether_py/
* License: Apache Software License 2.0


.. README_FEATURES

Features
--------

* ``ether_py`` provides a general Python command line interface (CLI)
  built on the OpenStack
  `cliff -- Command Line Interface Formulation Framework <https://github.com/openstack/cliff>`_.
* ``cliff`` provides many useful features like modularizing subcommands into
  groups, built-in help for internally documenting commands, and producing
  output in clean tabular form or in one of several data formats you can
  feed into other tools or automation platforms.
* `Sphinx <http://www.sphinx-doc.org/>`_ documentation for generation with `ReadTheDocs <https://readthedocs.com>`_
  including ``cliff`` autoprogram `Sphinx integration <https://docs.openstack.org/cliff/latest/user/sphinxext.html>`_
  for documenting commands from the same ``--help`` output you can get at the command line.
* Preconfigured for unit testing with `pytest <https://docs.pytest.org/en/stable/>`_,
  Python security vulnerability scanning with `bandit <https://bandit.readthedocs.io>`_,
  integration and system testing with BATS (`bats-core <https://bats-core.readthedocs.io>`_),
  and Python library dependency security scanning with GitHub's
  `dependabot <https://docs.github.com/en/code-security/supply-chain-security/configuring-dependabot-security-updates>`_.
* Uses `Tox <https://tox.readthedocs.io/>`_ for testing against Python 3.6, 3.7, 3.8, and 3.9.
* Set up for version number bumping with a single command using `bump2version <https://github.com/c4urself/bump2version>`_.
* Set up for `GitHub Actions <https://docs.github.com/en/actions/learn-github-actions/introduction-to-github-actions>`_
  workflow processing for automatic testing.
* The GitHub Actions workflow will also auto-release packages to `PyPI <https://pypi.org/>`_ or
  `Test PyPI <https://test.pypi.org>`_ when you push a new version tag on the ``master`` branch, or a
  special ``rc`` tag on the ``develop`` branch.


Contact
-------

Dave Dittrich <dave.dittrich@gmail.com>

.. |copy|   unicode:: U+000A9 .. COPYRIGHT SIGN

Copyright |copy| 2021 Dave Dittrich. All rights reserved.

Credits
-------

This package was created with `Cookiecutter
<https://github.com/cookiecutter/cookiecutter>`_ from the
<https://davedittrich/cookiecutter-cliffapp-template.git> project template.  It
derives some of its features and inspiration from
<https://github.com/veit/cookiecutter-namespace-template> and
<https://github.com/audreyfeldroy/cookiecutter-pypackage>.


.. EOF
