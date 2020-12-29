import os
import shutil
import subprocess
from pathlib import Path

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

    if 'dev' not in version and 'rc' not in version:
        version_string = f'v{version}'

        assert_file_contains_string(file_path=Path(PACKAGE_ROOT, 'README.md'), string=version_string)

    assert_file_contains_string(file_path=Path(PACKAGE_ROOT, 'pyproject.toml'), string=f'version = "{version}~ynh')
    assert_file_contains_string(file_path=Path(PACKAGE_ROOT, 'pyproject.toml'), string=f'pyinventory = "=={version}"')
    assert_file_contains_string(file_path=Path(PACKAGE_ROOT, 'manifest.json'), string=f'"version": "{version}~ynh')


def test_poetry_check():
    poerty_bin = shutil.which('poetry')

    output = subprocess.check_output(
        [poerty_bin, 'check'],
        universal_newlines=True,
        env=os.environ,
        stderr=subprocess.STDOUT,
        cwd=str(PACKAGE_ROOT),
    )
    print(output)
    assert output == 'All set!\n'
