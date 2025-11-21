#!/bin/bash

# Test to create the python virtual env and install all requirements.
# Note: Maybe you didn't have all OS packages installed ;)

set -e

final_path="./local_test"

set -x

mkdir -p "${final_path}/"
python3 -m venv "${final_path}/venv"
source "${final_path}/venv/bin/activate"

$final_path/venv/bin/pip install --upgrade wheel pip
$final_path/venv/bin/pip install --no-deps -r "./conf/requirements.txt"
