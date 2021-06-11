.. _usage:

=====
Usage
=====

Subcommand groups in ``ether-py`` are divided by categories
reflecting specific features, data sources, etc.


Getting help
------------

To get help information on global command arguments and options, use
the ``help`` command or ``--help`` option flag. The usage documentation
below will detail help output for each command.

.. Can't just get --help output using autoprogram-cliff. :(
..
.. .. autoprogram-cliff:: lim
..    :application: lim
..    :arguments: --help

.. literalinclude:: ether-py-help.txt
    :language: console

..

Formatters
----------

The `cliff -- Command Line Interface Formulation Framework <https://github.com/openstack/cliff>`_
provides a set of formatting options that facilitate accessing and using stored
secrets in other applications. Data can be passed directly in a structured
format like CSV, or passed directly to programs like Ansible using JSON.

.. attention::

    The formatter options are shown in the ``--help`` output for individual
    commands.  For the purposes of this chapter, including the lengthy
    formatter options on every command would be quite repetitive and take up a
    lot of space.  For this reason, the formatter options will be suppressed
    for commands as documented below. You can see the differences
    `in this functional example <https://python-secrets.readthedocs.io/en/latest/usage.html#usage>`_.

..  [When you put in your first commands, replace the :command: references
..  below with your own commands as seen in the example referenced above.]

..     for commands as documented below.  The difference (**WITH** and **WITHOUT**
..     the formatting options) would look like this:
..
..     **WITH** formatting options
..
..         .. autoprogram-cliff:: ether_py
..            :command: cafe info
..
..     **WITHOUT** formatting options
..
..         .. autoprogram-cliff:: ether_py
..            :command: cafe info
..            :ignored: -f,-c,--quote,--noindent,--max-width,--fit-width,--print-empty,--sort-column
..
.. ..

Logging
-------

Cliff also includes a mechanism for writing log output from the program
to a user-specified file at runtime.  This is useful for debugging, as well
as for monitoring long-running actions.

Here is an example of logging output of the ``about`` command::

    $ ether-py -vvvv --log-file logfile about
    initialize_app
    [+] command line: /usr/local/Caskroom/miniconda/base/envs/test/bin/ether-py -vvvv --log-file logfile about
    prepare_to_run_command About
    ether-py version 2021.3.0rc1

    This program was bootstrapped from a ``cookiecutter`` template created
    by Dave Dittrich <dave.dittrich@gmail.com>:

        https://github.com/davedittrich/cookiecutter-cliffapp-template.git
        https://cookiecutter-cliffapp-template.readthedocs.io

    Author:    Dave Dittrich <dave.dittrich@gmail.com>
    Copyright: 2021, Dave Dittrich. All rights reserved.
    License:   Apache Software License 2.0
    URL:       https://pypi.python.org/pypi/{{cookiecutter.project_name}}
    [!] clean_up About

Here is what the output would look like::

    $ cat logfile
    [2021-06-08 14:31:57,050] DEBUG    ether-py initialize_app
    [2021-06-08 14:31:57,051] INFO     ether-py [+] command line: /usr/local/Caskroom/miniconda/base/envs/test/bin/ether-py -vvvv --log-file logfile about
    [2021-06-08 14:31:57,052] DEBUG    ether-py prepare_to_run_command About
    [2021-06-08 14:31:57,073] DEBUG    ether-py [!] clean_up About

..

Command groups
--------------

About
~~~~~

.. autoprogram-cliff:: ether_py
   :command: about
   :ignored: -f,-c,--quote,--noindent,--max-width,--fit-width,--print-empty,--sort-column

Block
~~~~~

.. autoprogram-cliff:: ether_py
   :command: block *
   :ignored: -f,-c,--quote,--noindent,--max-width,--fit-width,--print-empty,--sort-column

Contract
~~~~~~~~

.. autoprogram-cliff:: ether_py
   :command: contract *
   :ignored: -f,-c,--quote,--noindent,--max-width,--fit-width,--print-empty,--sort-column

Demo
~~~~

.. autoprogram-cliff:: ether_py
   :command: demo *
   :ignored: -f,-c,--quote,--noindent,--max-width,--fit-width,--print-empty,--sort-column

Eth
~~~

.. autoprogram-cliff:: ether_py
   :command: eth *
   :ignored: -f,-c,--quote,--noindent,--max-width,--fit-width,--print-empty,--sort-column

Net
~~~

.. autoprogram-cliff:: ether_py
   :command: net *
   :ignored: -f,-c,--quote,--noindent,--max-width,--fit-width,--print-empty,--sort-column

Solc
~~~~

.. autoprogram-cliff:: ether_py
   :command: solc *
   :ignored: -f,-c,--quote,--noindent,--max-width,--fit-width,--print-empty,--sort-column

Tx
~~

.. autoprogram-cliff:: ether_py
   :command: tx *
   :ignored: -f,-c,--quote,--noindent,--max-width,--fit-width,--print-empty,--sort-column


.. EOF
