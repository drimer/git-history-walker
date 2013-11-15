#!/bin/bash


# Parse arguments
while getopts "v" option; do
    case $option in
        v) verbose=true;;
    esac
done
shift $(($OPTIND-1))

# Import tests from bash files
own_dir="$(dirname "$0")"
for tests_file in $own_dir/tests-*.sh; do
    source $tests_file
done

# Execute tests
ret=0
for t in $(declare -F | awk '/ test_/ {print $3}'); do
    $t && {
	[[ "$verbose" == "true" ]] && echo "$t: PASSED";
    } || {
	[[ "$verbose" == "true" ]] && echo "$t: FAILED";
	ret=1;
    }
done

exit $ret
