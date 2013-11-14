SHELL := /bin/bash


check-pylint:
	find . -name "*.py" | xargs pylint --rcfile pylint.conf

check-tests:
	./tests/run-tests.sh

check: check-tests check-pylint
