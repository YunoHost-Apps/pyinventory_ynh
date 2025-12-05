import os
import shlex
import sys
import unittest.util
from pathlib import Path

import django
from bx_py_utils.test_utils.deny_requests import deny_any_real_request
from cli_base.cli_tools.verbosity import MAX_LOG_LEVEL, setup_logging
from django.core.management.commands.test import Command as DjangoTestCommand
from django_yunohost_integration.local_test import CreateResults, create_local_test
from django_yunohost_integration.path_utils import get_project_root
from rich import print  # noqa
from typeguard import install_import_hook


# Check type annotations via typeguard in all tests:
install_import_hook(packages=('pyinventory_ynh',))


def pre_configure_tests() -> None:
    print(f'Configure unittests via "load_tests Protocol" from {Path(__file__).relative_to(Path.cwd())}')

    # Hacky way to display more "assert"-Context in failing tests:
    _MIN_MAX_DIFF = unittest.util._MAX_LENGTH - unittest.util._MIN_DIFF_LEN
    unittest.util._MAX_LENGTH = int(os.environ.get('UNITTEST_MAX_LENGTH', 300))
    unittest.util._MIN_DIFF_LEN = unittest.util._MAX_LENGTH - _MIN_MAX_DIFF

    # Deny any request via docket/urllib3 because tests they should mock all requests:
    deny_any_real_request()

    # Display DEBUG logs in tests:
    setup_logging(verbosity=MAX_LOG_LEVEL)


def create_local_test_files(*, runserver=False) -> CreateResults:
    print('Compile YunoHost files...')
    result: CreateResults = create_local_test(
        django_settings_path=get_project_root() / 'conf' / 'settings.py',
        destination=get_project_root() / 'local_test',
        runserver=runserver,
        extra_replacements={
            '__ADMIN_EMAIL__': 'foo-bar@test.tld',
            '__DEFAULT_FROM_EMAIL__': 'django_app@test.tld',
            '__PATH__': 'app_path',  # Simulate installation into "/app_path/" !
        },
    )
    print('Local test files created:')
    print(result)
    return result


def setup_ynh_tests() -> None:
    # Import after "install_import_hook" to check type annotations:
    import pyinventory_ynh

    os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

    result = create_local_test_files(runserver=False)

    data_dir = str(result.data_dir_path)
    if data_dir not in sys.path:
        sys.path.insert(0, data_dir)

    django.setup()

    os.chdir(Path(pyinventory_ynh.__file__).parent)


def _run_django_test_cli(argv, exit_after_run=True):
    """
    Call the origin Django test manage command CLI and pass all args to it.
    """
    setup_ynh_tests()

    print('\nStart Django unittests with:')
    for default_arg in ('shuffle', 'buffer'):
        if default_arg not in argv and f'--no-{default_arg}' not in argv:
            argv.append(f'--{default_arg}')
    print(shlex.join(argv))
    print()

    test_command = DjangoTestCommand()

    test_command.run_from_argv(argv)
    if exit_after_run:
        sys.exit(0)


def load_tests(loader, tests, pattern):
    """
    Use unittest "load_tests Protocol" as a hook to setup test environment before running tests.
    https://docs.python.org/3/library/unittest.html#load-tests-protocol
    """
    pre_configure_tests()
    return loader.discover(start_dir=Path(__file__).parent, pattern=pattern)
