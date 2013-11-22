test_directory_does_not_exist() {
    $repo_dir="nonexistent_directory"
    ./git_history_walker.py --repo $repo_dir
    [[ $? == 3 ]] || {
	echo "Expected to fail with return code 3 because $dir does not exist." >&2;
	return 1;
    }
}

test_directory_is_not_a_git_repository() {
    $repo_dir="/tmp/tmp-$RANDOM"
    mkdir $repo_dir
    ./git_history_walker.py --repo $repo_dir
    [[ $? == 3 ]] || {
	echo "Expected to fail with return code 3 because $dir is not a repository." >&2;
	return 1;
    }
}

test_current_directory_is_used_by_default() {
    $repo_dir="test-repo"
    
}
