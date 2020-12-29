SHELL := /bin/bash

all: help

help:
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z0-9 -]+:.*?## / {printf "\033[36m%-22s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

check-poetry:
	@if [[ "$(shell poetry --version 2>/dev/null)" == *"Poetry"* ]] ; \
	then \
		echo "Poetry found, ok." ; \
	else \
		echo 'Please install poetry first, with e.g.:' ; \
		echo 'make install-poetry' ; \
		exit 1 ; \
	fi

install-poetry:  ## install or update poetry
	pip3 install -U pip
	pip3 install -U poetry

install: check-poetry  ## install project via poetry
	poetry install

update: install-poetry  ## update the sources and installation and generate "conf/requirements.txt"
	poetry run pip install -U pip
	poetry update
	poetry export -f requirements.txt --output conf/requirements.txt

local-test: check-poetry  ## Run local_test.py to run the project locally
	poetry run ./local_test.py

local-diff-settings:  ## Run "manage.py diffsettings" with local test
	poetry run python3 local_test/opt_yunohost/manage.py diffsettings


##############################################################################

.PHONY: help check-poetry install-poetry install update local-test