import sys

from cli_base.cli_tools.dev_tools import run_coverage, run_nox, run_unittest_cli
from cli_base.cli_tools.subprocess_utils import verbose_check_call
from cli_base.cli_tools.test_utils.snapshot import UpdateTestSnapshotFiles
from cli_base.tyro_commands import TyroVerbosityArgType
from django_yunohost_integration.path_utils import get_project_root

from pyinventory_ynh.cli_dev import app
from pyinventory_ynh.tests import _run_django_test_cli


@app.command
def mypy(verbosity: TyroVerbosityArgType):
    """Run Mypy (configured in pyproject.toml)"""
    verbose_check_call('mypy', '.', cwd=get_project_root(), verbose=verbosity > 0, exit_on_error=True)


@app.command
def update_test_snapshot_files(verbosity: TyroVerbosityArgType):
    """
    Update all test snapshot files (by remove and recreate all snapshot files)
    """
    with UpdateTestSnapshotFiles(root_path=get_project_root(), verbose=verbosity > 0):
        # Just recreate them by running tests:
        run_unittest_cli(
            extra_env=dict(
                RAISE_SNAPSHOT_ERRORS='0',  # Recreate snapshot files without error
            ),
            verbose=verbosity > 1,
            exit_after_run=False,
        )


@app.command  # Dummy command
def test():
    """
    Run unittests
    """
    _run_django_test_cli(argv=sys.argv, exit_after_run=True)


@app.command  # Dummy command
def coverage():
    """
    Run tests and show coverage report.
    """
    run_coverage()


@app.command  # Dummy "nox" command
def nox():
    """
    Run nox
    """
    run_nox()
