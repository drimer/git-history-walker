#!/bin/bash


own_dir="$(dirname "$0")"
for tests_file in $own_dir/tests-*.sh; do
    source $tests_file
done

ret=0
for t in $(declare -F | awk '/ test_/ {print $3}'); do
    $t || ret=1
done

exit $ret
