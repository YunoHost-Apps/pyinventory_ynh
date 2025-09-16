from cli_base.cli_tools.code_style import assert_code_style
from cli_base.tyro_commands import TyroVerbosityArgType
from django_yunohost_integration.path_utils import get_project_root

from pyinventory_ynh.cli_dev import app


@app.command
def lint(verbosity: TyroVerbosityArgType = 1):
    """
    Check/fix code style by run: "ruff check --fix"
    """
    assert_code_style(package_root=get_project_root(), verbose=bool(verbosity), sys_exit=True)
