test_branch_without_base_branch() {
    cat >expected-output <<-EOF
ca9b647c34951727987c47adf13cf673aa2907fa
ec29da1c16d035054c625b9b49f916b2f498b264
94cce1dae5b4fd38ad2a85820973282a378a755c
e51da7d1ab35793d01898455a0b3503880a4e57b
f8c4362781b8115ff8702b67c989d81d371d0134
09d9e04800e6267c9a30fa5d571c68fc50c5cabe
EOF

    diff -u \
	expected-output \
	<(./git_history_walker.py --repo test-repo --branch devel \
	-- git rev-parse --revs-only HEAD)
}

test_branch_with_valid_base_branch() {
    cat >expected-output <<EOF
ca9b647c34951727987c47adf13cf673aa2907fa
ec29da1c16d035054c625b9b49f916b2f498b264
94cce1dae5b4fd38ad2a85820973282a378a755c
EOF

    diff -u \
	expected-output \
	<(./git_history_walker.py --repo test-repo --branch devel \
	--from-branch master -- git rev-parse --revs-only HEAD)
}
