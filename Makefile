SHELL := /bin/bash


check-pylint:
	find . -name "*.py" | xargs pylint --rcfile pylint.conf
