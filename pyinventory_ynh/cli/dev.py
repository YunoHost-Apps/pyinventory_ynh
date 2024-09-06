"""
    CLI for development
"""

import logging
import shlex
import sys
from pathlib import Path

import rich_click as click
from cli_base.cli_tools import code_style
from cli_base.cli_tools.dev_tools import run_coverage, run_tox
from cli_base.cli_tools.subprocess_utils import verbose_check_call
from cli_base.cli_tools.test_utils.snapshot import UpdateTestSnapshotFiles
from cli_base.cli_tools.verbosity import OPTION_KWARGS_VERBOSE
from cli_base.cli_tools.version_info import print_version
from cli_base.run_pip_audit import run_pip_audit
from django.core.management.commands.test import Command as DjangoTestCommand
from django_yunohost_integration.local_test import create_local_test
from django_yunohost_integration.path_utils import get_project_root
from manageprojects.utilities.publish import publish_package
from rich import print
from rich.console import Console
from rich.traceback import install as rich_traceback_install
from rich_click import RichGroup

import pyinventory_ynh
from pyinventory_ynh import constants
from pyinventory_ynh.tests import setup_ynh_tests


logger = logging.getLogger(__name__)


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


class ClickGroup(RichGroup):  # FIXME: How to set the "info_name" easier?
    def make_context(self, info_name, *args, **kwargs):
        info_name = './dev-cli.py'
        return super().make_context(info_name, *args, **kwargs)


@click.group(
    cls=ClickGroup,
    epilog=constants.CLI_EPILOG,
)
def cli():
    pass


@cli.command()
@click.option('-v', '--verbosity', **OPTION_KWARGS_VERBOSE)
def mypy(verbosity: int):
    """Run Mypy (configured in pyproject.toml)"""
    verbose_check_call('mypy', '.', cwd=get_project_root(), verbose=verbosity > 0, exit_on_error=True)


@cli.command()
def install():
    """
    Run pip-sync and install 'pyinventory_ynh' via pip as editable.
    """
    verbose_check_call('pip-sync', get_project_root() / 'requirements.dev.txt')
    verbose_check_call('pip', 'install', '--no-deps', '-e', '.')


@cli.command()
@click.option('-v', '--verbosity', **OPTION_KWARGS_VERBOSE)
def pip_audit(verbosity: int):
    """
    Run pip-audit check against current requirements files
    """
    run_pip_audit(base_path=get_project_root(), verbosity=verbosity)


@cli.command()
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

    run_pip_audit(base_path=get_project_root())

    # Install new dependencies in current .venv:
    verbose_check_call(bin_path / 'pip-sync', 'requirements.dev.txt')


@cli.command()
def publish():
    """
    Build and upload this project to PyPi
    """
    try:
        _run_django_test_cli(argv=sys.argv, exit_after_run=True)  # Don't publish a broken state
    except SystemExit as err:
        assert err.code == 0, f'Exit code is not 0: {err.code}'

    publish_package(
        module=pyinventory_ynh,
        package_path=get_project_root(),
        distribution_name='pyinventory_ynh',
    )


@cli.command()
@click.option('--color/--no-color', **OPTION_ARGS_DEFAULT_TRUE)
@click.option('-v', '--verbosity', **OPTION_KWARGS_VERBOSE)
def fix_code_style(color: bool, verbosity: int):
    """
    Fix code style of all pyinventory_ynh source code files via darker
    """
    code_style.fix(package_root=get_project_root(), darker_color=color, darker_verbose=verbosity > 0)


@cli.command()
@click.option('--color/--no-color', **OPTION_ARGS_DEFAULT_TRUE)
@click.option('-v', '--verbosity', **OPTION_KWARGS_VERBOSE)
def check_code_style(color: bool, verbosity: int):
    """
    Check code style by calling darker + flake8
    """
    code_style.check(package_root=get_project_root(), darker_color=color, darker_verbose=verbosity > 0)


@cli.command()
def update_test_snapshot_files():
    """
    Update all test snapshot files (by remove and recreate all snapshot files)
    """
    with UpdateTestSnapshotFiles(root_path=get_project_root(), verbose=True):
        # Just recreate them by running tests:
        _run_django_test_cli(argv=sys.argv, exit_after_run=False)


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


@cli.command()  # Dummy command
def test():
    """
    Compile YunoHost files and run Django unittests
    """
    _run_django_test_cli(argv=sys.argv, exit_after_run=True)


@cli.command()  # Dummy command
def coverage():
    """
    Run tests and show coverage report.
    """
    run_coverage()


@cli.command()  # Dummy "tox" command
def tox():
    """
    Run tox
    """
    run_tox()


@cli.command()
def version():
    """Print version and exit"""
    # Pseudo command, because the version always printed on every CLI call ;)
    sys.exit(0)


@cli.command()
def local_test():
    """
    Build a "local_test" YunoHost installation and start the Django dev. server against it.
    """
    create_local_test(
        django_settings_path=get_project_root() / 'conf' / 'settings.py',
        destination=get_project_root() / 'local_test',
        runserver=True,
        extra_replacements={
            '__DEBUG_ENABLED__': '1',
        },
    )


@cli.command()
def diffsettings():
    """
    Run "diffsettings" manage command against a "local_test" YunoHost installation.
    """
    destination = get_project_root() / 'local_test'
    create_local_test(
        django_settings_path=get_project_root() / 'conf' / 'settings.py',
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


def main():
    print_version(pyinventory_ynh)

    if len(sys.argv) >= 2:
        # Check if we can just pass a command call to origin CLI:
        command = sys.argv[1]
        command_map = {
            'test': _run_django_test_cli,
            'tox': run_tox,
            'coverage': run_coverage,
        }
        if real_func := command_map.get(command):
            real_func(argv=sys.argv, exit_after_run=True)

    console = Console()
    rich_traceback_install(
        width=console.size.width,  # full terminal width
        show_locals=True,
        suppress=[click],
        max_frames=2,
    )

    print('Execute Click CLI')
    cli()
