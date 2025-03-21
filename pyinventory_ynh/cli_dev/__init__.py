"""
CLI for development
"""

import importlib
import logging
import sys

from cli_base.autodiscover import import_all_files
from cli_base.cli_tools.dev_tools import run_coverage, run_nox
from cli_base.cli_tools.rich_utils import rich_traceback_install
from cli_base.cli_tools.version_info import print_version
from typeguard import install_import_hook
from tyro.extras import SubcommandApp

import pyinventory_ynh
from pyinventory_ynh import constants
from pyinventory_ynh.tests import _run_django_test_cli


# Check type annotations via typeguard in all tests.
# Sadly we must activate this here and can't do this in ./tests/__init__.py
install_import_hook(packages=('pyinventory_ynh',))

# reload the module, after the typeguard import hook is activated:
importlib.reload(pyinventory_ynh)


logger = logging.getLogger(__name__)


app = SubcommandApp()


# Register all CLI commands, just by import all files in this package:
import_all_files(package=__package__, init_file=__file__)


@app.command
def version():
    """Print version and exit"""
    # Pseudo command, because the version always printed on every CLI call ;)
    sys.exit(0)


def main():
    print_version(pyinventory_ynh)
    rich_traceback_install()

    if len(sys.argv) >= 2:
        # Check if we can just pass a command call to origin CLI:
        command = sys.argv[1]
        command_map = {
            'test': _run_django_test_cli,
            'nox': run_nox,
            'coverage': run_coverage,
        }
        if real_func := command_map.get(command):
            real_func(argv=sys.argv, exit_after_run=True)

    app.cli(
        prog='./dev-cli.py',
        description=constants.CLI_EPILOG,
        use_underscores=False,  # use hyphens instead of underscores
        sort_subcommands=True,
    )
