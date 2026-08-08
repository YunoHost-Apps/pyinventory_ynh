#!/bin/bash

# Test to create the python virtual env and install all requirements.
# Note: Maybe you didn't have all OS packages installed ;)
#
# This is similar to the myynh_setup_python_venv() function in scripts/_common.sh

set -e

data_dir="./local_test"

set -x

mkdir -p "${data_dir}/"

export VIRTUAL_ENV="$data_dir/.venv"
export UV_VENV="$data_dir/.venv"

uv venv --python python3.14 --clear "$data_dir/.venv"

"$data_dir/.venv/bin/python3" -VV

uv pip sync "./conf/pylock.toml"

"$data_dir/.venv/bin/django-admin" --version
