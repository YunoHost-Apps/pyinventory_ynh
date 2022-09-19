import difflib
import os
import shutil
import subprocess
from pathlib import Path

import tomli
from django_tools.serve_media_app.utils import clean_filename
from django_tools.unittest_utils.assertments import assert_is_dir, assert_is_file
from django_tools.unittest_utils.project_setup import check_editor_config

import inventory


PACKAGE_ROOT = Path(__file__).parent.parent


def assert_file_contains_string(file_path, string):
    with file_path.open('r') as f:
        for line in f:
            if string in line:
                return
    raise AssertionError(f'File {file_path} does not contain {string!r} !')


def test_version():
    upstream_version = inventory.__version__

    pyproject_toml_path = Path(PACKAGE_ROOT, 'pyproject.toml')
    pyproject_toml = tomli.loads(pyproject_toml_path.read_text(encoding='UTF-8'))
    pyproject_version = pyproject_toml['tool']['poetry']['version']
    assert pyproject_version.startswith(f'{upstream_version}+ynh')

    # pyproject.toml needs a PEP 440 conform version and used "+ynh"
    # the YunoHost syntax is: "~ynh", just "convert this:
    manifest_version = pyproject_version.replace('+', '~')

    assert_file_contains_string(
        file_path=Path(PACKAGE_ROOT, 'manifest.json'),
        string=f'"version": "{manifest_version}"',
    )


def poetry_check_output(*args):
    poerty_bin = shutil.which('poetry')

    output = subprocess.check_output(
        (poerty_bin,) + args,
        text=True,
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
    requirements_txt = PACKAGE_ROOT / 'conf' / 'requirements.txt'
    assert_is_file(requirements_txt)

    output = poetry_check_output('export', '-f', 'requirements.txt')
    assert 'Warning' not in output

    current_content = requirements_txt.read_text()

    diff = '\n'.join(
        difflib.unified_diff(
            current_content.splitlines(),
            output.splitlines(),
            fromfile=str(requirements_txt),
            tofile='FRESH EXPORT',
        )
    )
    print(diff)
    assert diff == '', f'{requirements_txt} is not up-to-date! (Hint: call: "make update")'


def test_screenshot_filenames():
    """
    https://forum.yunohost.org/t/yunohost-bot-cant-handle-spaces-in-screenshots/19483
    """
    screenshot_path = PACKAGE_ROOT / 'doc' / 'screenshots'
    assert_is_dir(screenshot_path)
    renamed = []
    for file_path in screenshot_path.iterdir():
        file_name = file_path.name
        cleaned_name = clean_filename(file_name)
        if cleaned_name != file_name:
            new_path = file_path.with_name(cleaned_name)
            file_path.rename(new_path)
            renamed.append(f'{file_name!r} renamed to {cleaned_name!r}')
    assert not renamed, f'Bad screenshots file names found: {", ".join(renamed)}'


def test_check_editor_config():
    check_editor_config(package_root=PACKAGE_ROOT)
