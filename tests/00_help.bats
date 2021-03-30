load test_helper

setup() {
    true
}

teardown() {
    true
}

@test "\"ether_py about\" contains \"version\"" {
    run bash -c "$ETHER_PY about"
    assert_output --partial 'version'
}

@test "'ether_py help' can load all entry points" {
    run bash -c "$ETHER_PY help 2>&1"
    refute_output --partial "Could not load EntryPoint"
}

@test "\"lim cafe --help\" properly lists subcommands" {
    run bash -c "$LIM cafe --help"
    assert_output 'Command "ether_py" matches:
  ether_py about'
}

@test "'ether_py --version' works" {
    run $ETHER_PY --version
    assert_output --partial "ether_py "
}

# vim: set ts=4 sw=4 tw=0 et :
