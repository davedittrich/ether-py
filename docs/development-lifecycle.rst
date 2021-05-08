Development Lifecycle Tasks
===========================

This section covers the tasks at various stages in the lifecycle of a Python
project.

Development Testing
-------------------

GitHub Actions are configured in the ``.github/workflows/test-build-publish.yml`` file
to always run tests when you ``push`` to GitHub.

.. literalinclude:: ../.github/workflows/test-build-publish.yml
    :start-after: # [1-test-build-publish]
    :end-before: # ![1-test-build-publish]

As you can see, the command it runs is the same one you would run at
the command line to test locally:

    .. code-block:: bash

        $ make test

    ..

.. note::

    When you are about to make a release it is always a good idea to make
    *sure* that all tests pass *before* you bump the version number or tag a
    test release and then ``push`` to trigger the release.

    At the minimum, get used to running the ``pep8`` Python syntax checks as
    you edit your code, as well as use a linter in your integrated development
    environment editor (such as VSCode).  You can do this with::

        $ tox -e pep8


    It is easier to fix any ``pep8`` (or ``bandit``) findings and commit working
    changes *before* you push than it is to deal with the GitHub Actions failure
    and repeat the tagging and/or version bumping.

..

Version numbering
-----------------

This repository is set up to use date-based version numbers that start
with the full year, followed by the release month and patch release
within that month. The first release in February of 2021 would thus
be ``v2021.2.0``.

The release version numbers are handled with ``bump2version`` as configured
in ``setup.cfg``. The current contents of that file are:

.. literalinclude:: ../setup.cfg
    :start-after: # [1-setup.cfg]
    :end-before:  # ![1-setup.cfg]

To understand how you are going to control devtest and full release numbers,
let's assume the assume the last full release was made in March 2021 and the
corresponding version number is currently set as follows::

    $ cat VERSION
    2021.3.0

Version numbers are generated using `setuptools_scm
<https://pypi.org/project/setuptools-scm/>`_. When you are doing development in
the Git repo directory, this will result in accurate version numbers
that reflect the *next* patch number or release candidate number,
along with specifics of the Git commits following the previous tag.
Let's say those tags look like this::

    $ git tag -l | grep v2021.3
    v2021.3.0
    v2021.3.1rc1
    v2021.3.1rc2
    v2021.3.1rc3

Given the last release candidate was ``v2021.3.1rc3``, the final component of
the current development version number would be ``1rc4`` and in this example
the repo is sitting at ten commits past the last tag, which was commit
``g9a790a9`` and the version number was generated on the 29th of March::

    $ python setup.py --version
    2021.3.1rc4.dev10+g9a790a9.d20210329



Releasing on PyPI or Test PyPI
------------------------------

The GitHub Actions workflow file (``../.github/workflows/test-build-publish.yml``)
is also set up to publish artifacts to PyPI or Test PyPi
based on tags.

.. literalinclude:: ../.github/workflows/test-build-publish.yml
    :language: yaml
    :dedent: 4
    :start-after: # [2-test-build-publish]
    :end-before: # ![2-test-build-publish]

You must have first configured GitHub encrypted secrets named
``PYPI_PASSWORD`` and ``TEST_PYPI_PASSWORD`` before the publish steps
will succeed.

Select *Settings** in your GitHub project page, then select *Secrets*
from the menu on the left. Create a new secret named ``TEST_PYPI_PASSWORD``
and open a new browser tab to https://test.pypi.org/ and log into your
account.

Select **Account settings** on Test PyPI from the menu on the left, then
then choose **Create a token for yourprojectname**. Use the name
``TEST_PYPI_PASSWORD`` for the token, select your project for the scope,
then **Add token**. You will only be able to see the token value once. Copy
it and enter it in the **Value** field in the GitHub project window.

Repeat the same process for PyPI using ``PYPI_PASSWORD``.

For Every Release
~~~~~~~~~~~~~~~~~

#. Update ``HISTORY.rst`` by analyzing your commit messages since the
   last release and summarizing the highlights.

    .. note::

        While there are tools you can use to auto-generate ``ChangeLog`` files,
        using every Git commit message is a little too verbose.


#. Commit the changes:

    .. code-block:: bash

        $ git add HISTORY.rst
        $ git commit -m "Changelog for upcoming release 2021.3.1"

    ..


For Test Releases
~~~~~~~~~~~~~~~~~

To publish a test release on the ``develop`` branch, you only need to add
an annotated tag with ``rc`` in the tag as we saw earlier.

The next candidate release tag in March following the example above would
thus be ``v2021.3.1rc4``::

    $ git tag -a v2021.3.rc4


For Full Releases
~~~~~~~~~~~~~~~~~

Full releases are controlled with ``bump2version``.

#. Since version numbering is set up using the year and month as the first
   two components, you only need to bump the patch component when doing
   new releases.

    .. code-block:: bash

        $ bump2version patch

    ..

   This would result in a new version number of ``2021.3.1``.

#. Install the package again for local development, but with the new version
   number:

    .. code-block:: bash

        $ make install-active

    ..

#. Push the commit:

    .. code-block:: bash

        $ git push

    ..

#. Push the tags, creating the new release on both GitHub and PyPI:

    .. code-block:: bash

        $ git push --tags

    ..

