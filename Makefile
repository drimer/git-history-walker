SHELL := /bin/bash


check-pylint:
	find . -name "*.py" | xargs pylint --rcfile pylint.conf

check-tests:
	./tests/run-tests.sh -v

check: check-tests check-pylint

clean:
	find . -regex ".*~\|.*.pyc" | xargs rm $f
	rm -rf tests/test-results/
