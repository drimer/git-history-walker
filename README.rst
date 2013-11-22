git-history-walker
==================

This is a simple script that will allow a user walk through a branch in a git
repository running commands.

This can be useful, for example, if we follow a peer-code review process in a
team and we need ensure our commits follow certain standards and rules. It's
easy to dispose of a home-made tool that runs a test suite, but it would be
run only on the commit our repository is checked out on the moment. In cases
like that, using git-history-walker.py makes this job easier.

All it will do is walk through the branch you're interested in, and run the
command you want on every single commit.

An example of usage:

    ./git-history-walker.py --branch development -- ./run_my_test_suite.sh

For more information on the available options, please run:

    ./git-history-walker.py -h