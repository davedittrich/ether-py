Development Lifecycle Tasks
===========================

This section covers tasks related to software development and release.

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

This repository is set up to use date based, or `calendar versioning
<https://calver.or>`_, for release version numbers. Version numbers use the
full **year** as the first (major) component, the **month** as the second
(minor) component, and patch releases using the third (normal patch)
component.

To illustrate how this works for development release candidate and full
release version numbers, let's assume the last full release was made in
March 2021 and there was only one release.  The corresponding version
number would be reflected in the ``VERSION`` file this way::

    $ cat VERSION
    2021.3.0

When you build the package with ``setup.py``, or when the ``ether-py`` program
wants to get the version number, they both use `setuptools_scm
<https://pypi.org/project/setuptools-scm/>`_.

Someone running ``ether-py --version`` after installing the program with
``python -m pip install ether-py`` will get a version number similar to
the example above::

    $ ether-py --version
    ether-py 2021.3.0

When you are developing in a clone of the GitHub repo, the result will
be a more precise version number that reflects the *next* patch number or
release candidate number, including specifics about the state of the Git repo
beyond the previous tag.

Let's say tags in the repo look like this::

    $ git tag -l | grep v2021.3
    v2021.3.0
    v2021.3.1rc1
    v2021.3.1rc2
    v2021.3.1rc3

Given the last release candidate was ``v2021.3.1rc3``, the final component of
the *current* development version number would be ``1rc4``. If the repo is
sitting at ten commits past the last tag with the last commit having hash
``g9a790a9``, the resulting version number as generated on the 29th of March
would look like this::

    $ python setup.py --version
    2021.3.1rc4.dev10+g9a790a9.d20210329

The version number string exists in several files, which all need to be updated
at the same time in a consistent manner. The program ``bump2version`` handles
that task as configured in the file ``setup.cfg``.

The contents of that file at the time this document was generated are:

.. literalinclude:: ../setup.cfg
    :start-after: # [1-setup.cfg]
    :end-before:  # ![1-setup.cfg]

..

.. warning::

    If you need to add a new file containing the version number, make sure to
    add the file path to this file.

..

Releasing on PyPI or Test PyPI
------------------------------

The GitHub Actions workflow file (``.github/workflows/test-build-publish.yml``)
is set up to publish artifacts to PyPI or Test PyPi based on pushed tags.  Here
is the portion of the file that handles this task.

.. literalinclude:: ../.github/workflows/test-build-publish.yml
    :language: yaml
    :dedent: 4
    :start-after: # [2-test-build-publish]
    :end-before: # ![2-test-build-publish]

Before this will work, you must have first created a token named
``ETHERPY_TEST_PYPI_PASSWORD`` on Test PyPI and another named
``ETHERPY_PYPI_PASSWORD`` on PyPI and stored them both in *encrypted
secrets* within your GitHub repo.

.. note::

   You will be copying and pasting the token values from one system to another,
   and we will be limiting the scope of the tokens to the *project* level and
   not for your entire account. This means one token per GitHub project per
   package index.  It is best to use the same token names on both GitHub and
   Test PyPI or PyPI, for consistency and less confusion later on.

   You may also want to use separate browser windows to have them visible
   at the same time to ensure the right tokens are used.

..

#. Open a browser tab and log into your GitHub account. Go to your project's
   repo page, then select **Settings**, then select **Secrets** from the
   menu on the left.

#. Open a new browser tab to https://test.pypi.org/ and log into your account.
   Select **Account settings** on Test PyPI from the menu on the left, then
   then choose **Create a token for ether-py**. Enter
   ``ETHERPY_TEST_PYPI_PASSWORD`` for the token name. For scope, select this
   project to limit the scope.  Finally, press **Add token**. You will only be
   able to see the token value once.  Get ready to copy it to paste into the
   **Value** field in the GitHub project window.

   .. image:: images/test-pypi-token.png

#. In the GitHub window, create a new secret named ``ETHERPY_TEST_PYPI_PASSWORD``.
   Paste the token into the **Value** field, then select **Add Secret**.

   .. image:: images/github-action-token.png

#. Repeat the same process for PyPI using the token name
   ``ETHERPY_PYPI_PASSWORD``.


For Every Release
~~~~~~~~~~~~~~~~~

The publishing workflow is triggered by pushing a new tag, so the
``push`` always has to be the *last* step in the release process.

Before doing that push, make sure you update ``HISTORY.rst`` by analyzing your
commit messages since the last release and summarizing the highlights.

.. note::

    While there are tools you can use to auto-generate ``ChangeLog`` files,
    using every Git commit message is a little too verbose.

..

Add and commit the changes:

.. code-block:: bash

    $ git add HISTORY.rst
    $ git commit -m "Changelog for upcoming release 2021.3.1"

..

.. warning::

   DO NOT FORGET to run ``make test`` when you think you are ready to
   make a release. This helps make sure no remaining bugs or coding
   errors will cause the GitHub workflow to fail before it gets to
   the publish step, which would require an additional tag following
   code fixes.

..

For Test Releases
~~~~~~~~~~~~~~~~~

To publish a test release on the ``develop`` branch, you only need to add
an annotated tag with ``rc`` in the tag string.  The next candidate release tag
in March following the example above would thus be ``v2021.3.1rc4``::

    $ git tag -a v2021.3.rc4

Pushing the tag will trigger the release to Test PyPI.

For Full Releases
~~~~~~~~~~~~~~~~~

Full releases are more involved.

First make sure that all tests pass and that you are satisfied all code and
documentation changes are ready. Then merge all the new commits into the
``master`` branch and resolve any merge conflicts.

If you are using the Git `HubFlow
<https://datasift.github.io/gitflow/TheHubFlowTools.html>`_ tool, you will now
start a new release with ``git hf release start`` with the new version number.

You are now ready to bump the version number in source files and update the
history file. Assuming we are starting with version ``2021.3.0``, there are
two cases we need to consider in terms of choosing the new release number.

#. If you are making a release *within the same month* as the prior
   release, the new version number will only need the patch
   component to be incremented. To go from ``2021.3.0`` to
   ``2021.3.1``, you just need to do::

       $ bump2version patch

#. If you are making release in a *different month or year* from
   the previous release, the new version number will have
   a different major and or minor number change.

   In the case where the release is in the *next* month (e.g., going from
   ``2021.3.0`` to ``2021.4.0``), you only need to do::

       $ bump2version minor

   If the time difference is longer than one month (e.g., going from
   ``2021.3.0`` to ``2021.8.0``), you need to do::

       $ bump2version --current-version $(cat VERSION) --new-version 2021.8.0 patch

If you are using the Git `HubFlow
<https://datasift.github.io/gitflow/TheHubFlowTools.html>`_ tool, do your
normal ``release finish`` and it will handle the tagging and pushing.
Otherwise, manually tag and push the ``master`` branch and associated tag::

    $ git tag -a v$(cat VERSION)
    $ git push && git push --tags

Either way, the pushed tag will create the new release on both GitHub and
PyPI.
