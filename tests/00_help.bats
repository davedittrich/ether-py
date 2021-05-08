load test_helper

setup() {
    true
}

teardown() {
    true
}

@test "\"ether-py about\" contains \"version\"" {
    run bash -c "$ETHER_PY about"
    assert_output --partial 'version'
}

@test "'ether-py help' can load all entry points" {
    run bash -c "$ETHER_PY help 2>&1"
    refute_output --partial "Could not load EntryPoint"
}

# vim: set ts=4 sw=4 tw=0 et :
