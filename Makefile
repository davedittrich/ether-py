# Makefile for ether-py (ether_py)

SHELL:=/bin/bash
VERSION:=$(shell cat VERSION)
CWD:=$(shell pwd)
PROJECT:=ether-py
MODULE:=ether_py
SLUG_ENV:="ETHERPY"
# Explicitly use 'python3' for OSs that stopped installing 'python'
# as Python 2.7.
PYTHON=python3


# Phony target to default action for just typing "make"
.PHONY: default
default: help

.PHONY: help
help:
	@echo 'usage: make [VARIABLE=value] [target [target..]]'
	@echo ''
	@echo 'test - generic target for both "test-tox" and "test-bats"'
	@echo 'test-tox - run tox tests'
	@echo 'test-bats - run Bats unit tests'
	@echo 'test-bats-runtime - run Bats runtime integration/system tests'
	@echo 'release - produce a pypi production release'
	@echo 'release-test - produce a pypi test release'
	@echo 'release-prep - final documentation preparations for release'
	@echo 'sdist - run "$(PYTHON) setup.py sdist"'
	@echo 'bdist_wheel - build a universal binary wheel'
	@echo 'twine-check - run "twine check"'
	@echo 'clean - remove build artifacts'
	@echo 'spotless - deep clean'
	@echo 'install - install pip package'
	@echo 'install-active - run "$(PYTHON) -m pip install -U ."'
	@echo 'docs-tests - generate bats test output for documentation'
	@echo 'docs-help - generate "$(PROJECT) help" output for documentation'
	@echo 'docs - build Sphinx docs'

#HELP test - run 'tox' for testing
.PHONY: test
test: test-tox
	@echo '[+] All tests succeeded'

.PHONY: test-tox
test-tox:
	@if [ -f .python_secrets_environment ]; then (echo '[!] Remove .python_secrets_environment prior to testing'; exit 1); fi
	@# See comment in tox.ini file.
	tox -e pep8,bandit,docs && tox -e py36,py37,py38,bats,pypi
	@-[[ -f ChangeLog ]] && git checkout ChangeLog || true

.PHONY: test-bats
test-bats: bats-libraries
	@if [ "$(TRAVIS)" != "true" ]; then \
		if ! type bats 2>/dev/null >/dev/null; then \
			echo "[-] Skipping bats tests"; \
		else \
			echo "[+] Running bats tests: $(shell cd tests && echo [0-9][0-9]*.bats)"; \
			PYTHONWARNINGS="ignore" bats --tap tests/[0-9][0-9]*.bats; \
		fi \
	 fi

.PHONY: test-bats-runtime
test-bats-runtime: bats-libraries
	@echo "[+] Running bats runtime tests: $(shell cd tests && echo runtime_[0-9][0-9]*.bats)"; \
	PYTHONWARNINGS="ignore" bats --tap tests/runtime_[0-9][0-9]*.bats

.PHONY: no-diffs
no-diffs:
	@echo 'Checking Git for uncommitted changes'
	git diff --quiet HEAD

#HELP release - package and upload a release to pypi
.PHONY: release
release: clean docs sdist bdist_wheel twine-check
	twine upload dist/* -r pypi

#HELP release-prep - final documentation preparations for release
.PHONY: release-prep
release-prep: install-active clean sdist docs-help docs-tests
	@echo 'Check in help text docs and ChangeLog?'

#HELP release-test - upload to "testpypi"
.PHONY: release-test
release-test: clean docs sdist bdist_wheel twine-check
	$(MAKE) no-diffs
	twine upload dist/* -r testpypi

#HELP sdist - build a source package
.PHONY: sdist
sdist: docs
	rm -f dist/.LATEST_TARGZ
	$(PYTHON) setup.py sdist
	(cd dist && ls -t *.tar.gz 2>/dev/null | head -n 1) > dist/.LATEST_TARGZ
	ls -lt dist/*.tar.gz

#HELP bdist_wheel - build a universal binary wheel
.PHONY: bdist_wheel
bdist_wheel:
	rm -f dist/.LATEST_WHEEL
	$(PYTHON) setup.py bdist_wheel --universal
	(cd dist && ls -t *.whl 2>/dev/null | head -n 1) > dist/.LATEST_WHEEL
	ls -lt dist/*.whl

#HELP twine-check
.PHONY: twine-check
twine-check: sdist
	twine check dist/"$(shell cat dist/.LATEST_TARGZ)"

#HELP clean - remove build artifacts
.PHONY: clean
clean:
	find . -name '*.pyc' -delete
	rm -rf docs/_build/{html,doctrees}
	rm -f ctu*-cache.json
	rm -rf dist build *.egg-info

#HELP spotless - deep clean
.PHONY: spotless
spotless: clean
	rm -rf .eggs .tox
	(cd docs && make clean)
	rm -rf tests/libs/{bats,bats-support,bats-assert}

#HELP install - install in required Python virtual environment (default $(REQUIRED_VENV))
.PHONY: install
install:
	@if [ ! -d $(VENV_DIR) ]; then \
		echo "Required virtual environment '$(REQUIRED_VENV)' not found."; \
		exit 1; \
	fi
	@if [ ! -e "$(VENV_DIR)/bin/python3" ]; then \
		echo "Cannot find $(VENV_DIR)/bin/python3"; \
		exit 1; \
	else \
		echo "Installing into $(REQUIRED_VENV) virtual environment"; \
		$(VENV_DIR)/bin/python3 -m pip uninstall -y $(PROJECT); \
		$(VENV_DIR)/bin/python3 setup.py install | grep -v 'already satisfied'; \
	fi

#HELP install-active - install in the active Python virtual environment
.PHONY: i
.PHONY: install-active
i install-active: bdist_wheel
	$(PYTHON) -m pip uninstall -y $(PROJECT)
	$(PYTHON) -m pip install -U "dist/$(shell cat dist/.LATEST_WHEEL)" | grep -v 'already satisfied'
	$(MAKE) docs-help
	-[[ -f ChangeLog ]] && git checkout ChangeLog || true

#HELP docs-tests - generate bats test output for documentation
.PHONY: docs-tests
PR=pr --omit-header --omit-pagination --page-width 80
docs-tests:
	$(MAKE) -B docs/test-tox.txt
	$(MAKE) -B docs/test-bats.txt
	$(MAKE) -B docs/test-bats-runtime.txt

docs/test-tox.txt:
	(echo '$$ make test-tox' && $(MAKE) test-tox) |\
	       $(PR) | tee docs/test-tox.txt

docs/test-bats.txt:
	$(MAKE) test-bats | $(PR) | tee docs/test-bats.txt

docs/test-bats-runtime.txt:
	(echo '$$ make test-bats-runtime' && $(MAKE) test-bats-runtime) |\
	       $(PR) | tee docs/test-bats-runtime.txt

#HELP docs-help - generate help output for documentation
.PHONY: docs-help
docs-help:
	(export $(SLUG_ENV)_DATA_DIR='/path/to/data'; \
	 unset BROWSER; \
	 $(PYTHON) -m $(MODULE) help) > docs/$(PROJECT)-help.txt

#HELP docs - build Sphinx docs (NOT INTEGRATED YET FROM OPENSTACK CODE BASE)
.PHONY: docs
docs: docs-help
	(export $(SLUG_ENV)_DATA_DIR='/path/to/data'; \
	 unset BROWSER; \
	 cd docs && \
	 make clean html)

#HELP examples - produce some example output for docs
.PHONY: examples
examples:
	$(PROJECT) --help

# Git submodules and subtrees are both a huge PITA. This is way simpler.

.PHONY: bats-libraries
bats-libraries: bats-core bats-support bats-assert

bats-core:
	@if ! bats --help | grep -q bats-core || [ ! -d tests/libs/bats-core ]; then \
		echo "[+] Cloning bats-core from GitHub"; \
		mkdir -p tests/libs/bats-core; \
		git clone https://github.com/bats-core/bats-core.git tests/libs/bats-core; \
		echo "[+] Installing bats-core in /usr/local with sudo"; \
		sudo tests/libs/bats-core/install.sh /usr/local; \
	 fi


bats-support:
	@[ -d tests/libs/bats-support ] || \
		(mkdir -p tests/libs/bats-support; git clone https://github.com/ztombol/bats-support tests/libs/bats-support)

bats-assert:
	@[ -d tests/libs/bats-assert ] || \
		(mkdir -p tests/libs/bats-assert; git clone https://github.com/ztombol/bats-assert tests/libs/bats-assert)

#EOF
