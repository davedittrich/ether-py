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

About
-----

.. autoprogram-cliff:: ether_py
   :command: about
   :ignored: -f,-c,--quote,--noindent,--max-width,--fit-width,--print-empty,--sort-column


.. EOF
