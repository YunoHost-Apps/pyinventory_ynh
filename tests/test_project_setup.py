import difflib
import os
import shutil
import subprocess
from pathlib import Path

from bx_py_utils.path import assert_is_file

import inventory


PACKAGE_ROOT = Path(__file__).parent.parent


def assert_file_contains_string(file_path, string):
    with file_path.open('r') as f:
        for line in f:
            if string in line:
                return
    raise AssertionError(f'File {file_path} does not contain {string!r} !')


def test_version():
    version = inventory.__version__

    assert_file_contains_string(file_path=Path(PACKAGE_ROOT, 'pyproject.toml'), string=f'version = "{version}~ynh')
    assert_file_contains_string(file_path=Path(PACKAGE_ROOT, 'pyproject.toml'), string=f'pyinventory = ">={version}"')
    assert_file_contains_string(file_path=Path(PACKAGE_ROOT, 'manifest.json'), string=f'"version": "{version}~ynh')


def poetry_check_output(*args):
    poerty_bin = shutil.which('poetry')

    output = subprocess.check_output(
        (poerty_bin,) + args,
        universal_newlines=True,
        env=os.environ,
        stderr=subprocess.STDOUT,
        cwd=str(PACKAGE_ROOT),
    )
    print(output)
    return output


def test_poetry_check():
    output = poetry_check_output('check')
    assert output == 'All set!\n'


def test_requirements_txt():
    requirements_txt = Path('conf', 'requirements.txt')
    assert_is_file(requirements_txt)

    output = poetry_check_output('export', '-f', 'requirements.txt')
    assert 'Warning' not in output

    current_content = requirements_txt.read_text()

    diff = '\n'.join(
        difflib.unified_diff(
            current_content.splitlines(), output.splitlines(),
            fromfile=str(requirements_txt), tofile='FRESH EXPORT'
        )
    )
    print(diff)
    assert diff == '', f'{requirements_txt} is not up-to-date! (Hint: call: "make update")'
