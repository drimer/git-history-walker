#!/usr/bin/env python

import argparse
import contextlib
import subprocess
import sys

from sh import git, pwd, cd, ErrorReturnCode


branch_name = 'multiple-state-machines'

# TODO: use a proper _cache variable to be more verbose
#       '_commits_in_master' is no intuitive at all
_commits_in_master = []


class InvalidDirectoryPath(Exception):
    pass



@contextlib.contextmanager
def cwd(path):
    previous_pwd = pwd().rstrip()
    try:
        cd(path)
    except OSError:
        raise InvalidDirectoryPath(
            'WARNING: did not change working directory to %s' % str(path))
    yield
    cd(previous_pwd)


def list_all_branch_commits(branch_name):
    output = git('rev-list', branch_name)
    return [c.strip() for c in output]


def commit_is_in_branch(commit_sha, branch_name):
    return commit_sha in list_all_branch_commits(branch_name)


def get_all_commits_in_branch(branch_name, from_branch=None):
    all_commits = list_all_branch_commits(branch_name)
    if from_branch:
        all_commits = [commit for commit in all_commits \
                           if not commit_is_in_branch(commit, from_branch)]
    return all_commits


@contextlib.contextmanager
def git_checkout(commit):
    # TODO: needs to stash, clean, go back to previous state, etc
    git('checkout', commit)
    yield


def parse_arguments(arguments):
    parser = argparse.ArgumentParser()
    parser.add_argument('--repo', '-r', dest='git_repository', default='.')
    parser.add_argument('--branch', '-b', dest='branch_name', default='master')
    parser.add_argument('--from-branch', dest='from_branch', default=None)
    parser.add_argument('command', nargs='+')
    return parser.parse_args(arguments)


def verify_options(options):
    if not options.from_branch:
        return

    try:
        git('show-branch', options.from_branch)
    except ErrorReturnCode as e:
        if e.exit_code == 128:
            print 'ERROR: --from-branch contains an invalid branch name'
            sys.exit(3)

def main(options):
    verify_options(options)

    with cwd(options.git_repository):
        for commit in get_all_commits_in_branch(
                options.branch_name, from_branch=options.from_branch):
            with git_checkout(commit):
                try:
                    return_code = subprocess.call(options.command)
                except (OSError, subprocess.CalledProcessError):
                    print 'Command %s failed on commit %s' % (
                        options.command, commit)
                    sys.exit(return_code)
                else:
                    if return_code != 0:
                        print 'Command %s failed on commit %s' % (
                            options.command, commit)
                        sys.exit(return_code)
                    

if __name__ == '__main__':
    options = parse_arguments(sys.argv[1:])
    # TODO: handle Ctrl+C events and revert repository to its previous state
    # TODO: redirect output from command to different file for each commit
    main(options)
