"""
    CLI for development
"""
import logging
import os
import sys
from pathlib import Path

import django
import rich_click as click
from bx_py_utils.path import assert_is_file
from cli_base.cli_tools.subprocess_utils import verbose_check_call
from cli_base.cli_tools.version_info import print_version
from django.core.management.commands.test import Command as DjangoTestCommand
from django_yunohost_integration.local_test import CreateResults, create_local_test
from manageprojects.utilities import code_style
from manageprojects.utilities.publish import publish_package
from rich import print  # noqa; noqa
from rich_click import RichGroup

import pyinventory_ynh


logger = logging.getLogger(__name__)


PACKAGE_ROOT = Path(pyinventory_ynh.__file__).parent.parent
assert_is_file(PACKAGE_ROOT / 'pyproject.toml')

OPTION_ARGS_DEFAULT_TRUE = dict(is_flag=True, show_default=True, default=True)
OPTION_ARGS_DEFAULT_FALSE = dict(is_flag=True, show_default=True, default=False)
ARGUMENT_EXISTING_DIR = dict(
    type=click.Path(exists=True, file_okay=False, dir_okay=True, readable=True, path_type=Path)
)
ARGUMENT_NOT_EXISTING_DIR = dict(
    type=click.Path(
        exists=False,
        file_okay=False,
        dir_okay=True,
        readable=False,
        writable=True,
        path_type=Path,
    )
)
ARGUMENT_EXISTING_FILE = dict(
    type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True, path_type=Path)
)
CLI_EPILOG = 'Project Homepage: https://github.com/YunoHost-Apps/pyinventory_ynh'


class ClickGroup(RichGroup):  # FIXME: How to set the "info_name" easier?
    def make_context(self, info_name, *args, **kwargs):
        info_name = './dev-cli.py'
        return super().make_context(info_name, *args, **kwargs)


@click.group(cls=ClickGroup, epilog=CLI_EPILOG)
def cli():
    pass


@click.command()
@click.option('--verbose/--no-verbose', **OPTION_ARGS_DEFAULT_FALSE)
def mypy(verbose: bool = True):
    """Run Mypy (configured in pyproject.toml)"""
    verbose_check_call('mypy', '.', cwd=PACKAGE_ROOT, verbose=verbose, exit_on_error=True)


cli.add_command(mypy)


@click.command()
@click.option('--verbose/--no-verbose', **OPTION_ARGS_DEFAULT_FALSE)
def coverage(verbose: bool = True):
    """
    Run and show coverage.
    """
    verbose_check_call('coverage', 'run', verbose=verbose, exit_on_error=True)
    verbose_check_call('coverage', 'combine', '--append', verbose=verbose, exit_on_error=True)
    verbose_check_call('coverage', 'report', '--fail-under=10', verbose=verbose, exit_on_error=True)
    verbose_check_call('coverage', 'xml', verbose=verbose, exit_on_error=True)
    verbose_check_call('coverage', 'json', verbose=verbose, exit_on_error=True)


cli.add_command(coverage)


@click.command()
def install():
    """
    Run pip-sync and install 'pyinventory_ynh' via pip as editable.
    """
    verbose_check_call('pip-sync', PACKAGE_ROOT / 'requirements.dev.txt')
    verbose_check_call('pip', 'install', '--no-deps', '-e', '.')


cli.add_command(install)


@click.command()
def safety():
    """
    Run safety check against current requirements files
    """
    verbose_check_call('safety', 'check', '-r', 'requirements.dev.txt')


cli.add_command(safety)


@click.command()
def update():
    """
    Update "requirements*.txt" dependencies files
    """
    bin_path = Path(sys.executable).parent

    verbose_check_call(bin_path / 'pip', 'install', '-U', 'pip')
    verbose_check_call(bin_path / 'pip', 'install', '-U', 'pip-tools')

    extra_env = dict(
        CUSTOM_COMPILE_COMMAND='./dev-cli.py update',
    )

    pip_compile_base = [
        bin_path / 'pip-compile',
        '--verbose',
        '--allow-unsafe',  # https://pip-tools.readthedocs.io/en/latest/#deprecations
        '--resolver=backtracking',  # https://pip-tools.readthedocs.io/en/latest/#deprecations
        '--upgrade',
        '--generate-hashes',
    ]

    # Only "prod" dependencies:
    verbose_check_call(
        *pip_compile_base,
        'pyproject.toml',
        '--output-file',
        'conf/requirements.txt',
        extra_env=extra_env,
    )

    # dependencies + "dev"-optional-dependencies:
    verbose_check_call(
        *pip_compile_base,
        'pyproject.toml',
        '--extra=dev',
        '--output-file',
        'requirements.dev.txt',
        extra_env=extra_env,
    )

    verbose_check_call(bin_path / 'safety', 'check', '-r', 'requirements.dev.txt')

    # Install new dependencies in current .venv:
    verbose_check_call(bin_path / 'pip-sync', 'requirements.dev.txt')


cli.add_command(update)


@click.command()
def publish():
    """
    Build and upload this project to PyPi
    """
    try:
        _run_django_test_cli()  # Don't publish a broken state
    except SystemExit as err:
        assert err.code == 0, f'Exit code is not 0: {err.code}'

    publish_package(
        module=pyinventory_ynh,
        package_path=PACKAGE_ROOT,
        distribution_name='pyinventory_ynh',
    )


cli.add_command(publish)


@click.command()
@click.option('--color/--no-color', **OPTION_ARGS_DEFAULT_TRUE)
@click.option('--verbose/--no-verbose', **OPTION_ARGS_DEFAULT_FALSE)
def fix_code_style(color: bool = True, verbose: bool = False):
    """
    Fix code style of all pyinventory_ynh source code files via darker
    """
    code_style.fix(package_root=PACKAGE_ROOT, color=color, verbose=verbose)


cli.add_command(fix_code_style)


@click.command()
@click.option('--color/--no-color', **OPTION_ARGS_DEFAULT_TRUE)
@click.option('--verbose/--no-verbose', **OPTION_ARGS_DEFAULT_FALSE)
def check_code_style(color: bool = True, verbose: bool = False):
    """
    Check code style by calling darker + flake8
    """
    code_style.check(package_root=PACKAGE_ROOT, color=color, verbose=verbose)


cli.add_command(check_code_style)


@click.command()
def update_test_snapshot_files():
    """
    Update all test snapshot files (by remove and recreate all snapshot files)
    """

    def iter_snapshot_files():
        yield from PACKAGE_ROOT.rglob('*.snapshot.*')

    removed_file_count = 0
    for item in iter_snapshot_files():
        item.unlink()
        removed_file_count += 1
    print(f'{removed_file_count} test snapshot files removed... run tests...')

    # Just recreate them by running tests:
    os.environ['RAISE_SNAPSHOT_ERRORS'] = '0'  # Recreate snapshot files without error
    try:
        _run_django_test_cli()
    finally:
        new_files = len(list(iter_snapshot_files()))
        print(f'{new_files} test snapshot files created, ok.\n')


cli.add_command(update_test_snapshot_files)


def _run_django_test_cli():
    """
    Call the origin Django test manage command CLI and pass all args to it.
    """
    os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

    print('Compile YunoHost files...')
    result: CreateResults = create_local_test(
        django_settings_path=PACKAGE_ROOT / 'conf' / 'settings.py',
        destination=PACKAGE_ROOT / 'local_test',
        runserver=False,
        extra_replacements={
            '__DEBUG_ENABLED__': '0',  # "1" or "0" string
            '__LOG_LEVEL__': 'INFO',
            '__ADMIN_EMAIL__': 'foo-bar@test.tld',
            '__DEFAULT_FROM_EMAIL__': 'django_app@test.tld',
        },
    )
    print('Local test files created:')
    print(result)

    data_dir = str(result.data_dir_path)
    if data_dir not in sys.path:
        sys.path.insert(0, data_dir)

    django.setup()

    os.chdir(Path(pyinventory_ynh.__file__).parent)

    test_command = DjangoTestCommand()
    test_command.run_from_argv(sys.argv)


@click.command()  # Dummy command
def test():
    """
    Compile YunoHost files and run Django unittests
    """
    _run_django_test_cli()


cli.add_command(test)


def _run_tox():
    verbose_check_call(sys.executable, '-m', 'tox', *sys.argv[2:])
    sys.exit(0)


@click.command()  # Dummy "tox" command
def tox():
    """
    Run tox
    """
    _run_tox()


cli.add_command(tox)


@click.command()
def version():
    """Print version and exit"""
    # Pseudo command, because the version always printed on every CLI call ;)
    sys.exit(0)


cli.add_command(version)


@click.command()
def local_test():
    """
    Build a "local_test" YunoHost installation and start the Django dev. server against it.
    """
    create_local_test(
        django_settings_path=PACKAGE_ROOT / 'conf' / 'settings.py',
        destination=PACKAGE_ROOT / 'local_test',
        runserver=True,
        extra_replacements={
            '__DEBUG_ENABLED__': '1',
        },
    )


cli.add_command(local_test)


@click.command()
def diffsettings():
    """
    Run "diffsettings" manage command against a "local_test" YunoHost installation.
    """
    destination = PACKAGE_ROOT / 'local_test'
    create_local_test(
        django_settings_path=PACKAGE_ROOT / 'conf' / 'settings.py',
        destination=destination,
        runserver=False,
        extra_replacements={
            '__DEBUG_ENABLED__': '1',
        },
    )
    app_path = destination / 'opt_yunohost'
    verbose_check_call(
        sys.executable,
        app_path / 'manage.py',
        'diffsettings',
        cwd=app_path,
    )


cli.add_command(diffsettings)


def main():
    print_version(pyinventory_ynh)

    print(f'{sys.argv=}')
    if len(sys.argv) >= 2:
        # Check if we just pass a command call
        command = sys.argv[1]
        if command == 'test':
            _run_django_test_cli()
            sys.exit(0)
        elif command == 'tox':
            _run_tox()
            sys.exit(0)

    print('Execute Click CLI')
    cli()
