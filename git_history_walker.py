#!/usr/bin/env python

import argparse
import contextlib
import subprocess
import sys

from sh import git, pwd, cd


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


def commit_is_in_master(commit_sha):
    # pylint: disable=W0603
    global _commits_in_master
    if not _commits_in_master:
        _commits_in_master = list_all_branch_commits('master')
    return commit_sha in _commits_in_master


def get_new_commits_in_branch(branch_name):
    all_commits = list_all_branch_commits(branch_name)
    return [commit for commit in all_commits if not commit_is_in_master(commit)]


@contextlib.contextmanager
def git_checkout(commit):
    # TODO: needs to stash, clean, go back to previous state, etc
    git('checkout', commit)
    yield

def parse_arguments(arguments):
    parser = argparse.ArgumentParser()
    parser.add_argument('--repo', '-r', dest='git_repository', default='.')
    parser.add_argument('--branch', '-b', dest='branch_name', default='master')
    parser.add_argument('command', nargs='+')
    return parser.parse_args(arguments)


def main(options):
    with cwd(options.git_repository):
        for commit in get_new_commits_in_branch(options.branch_name):
            with git_checkout(commit):
                print 'Running: %s on %s' % (options.command, commit)
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
