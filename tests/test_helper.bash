export OS=$(uname -s)
export PYTHONPATH=$(pwd)
export ETHER_PY="python3 -m ether_py --debug"

load 'libs/bats-support/load'
load 'libs/bats-assert/load'

# vim: set ts=4 sw=4 tw=0 et :
