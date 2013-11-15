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

# Prepare directory for test results
all_results_dir="test-results"
mkdir -p $all_results_dir

# Execute tests
ret=0
for t in $(declare -F | awk '/ test_/ {print $3}'); do
    test_results_dir="$all_results_dir/$t"
    mkdir -p $test_results_dir
    $t >"$test_results_dir/stdout.log" \
	2>"$test_results_dir/stderr.log"
    [[ $? == 0 ]] && {
	rm -r $test_results_dir;
	[[ "$verbose" == "true" ]] && echo "$t: PASSED";
    } || {
	[[ "$verbose" == "true" ]] && echo "$t: FAILED";
	ret=1;
    }
done

[[ $ret == 0 ]] && rm -r $all_results_dir

exit $ret
