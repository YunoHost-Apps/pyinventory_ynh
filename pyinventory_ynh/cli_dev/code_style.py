from cli_base.cli_tools import code_style
from cli_base.tyro_commands import TyroVerbosityArgType
from django_yunohost_integration.path_utils import get_project_root

from pyinventory_ynh.cli_dev import app


@app.command
def fix_code_style(verbosity: TyroVerbosityArgType, color: bool = True):
    """
    Fix code style of all pyinventory_ynh source code files via darker
    """
    code_style.fix(package_root=get_project_root(), darker_color=color, darker_verbose=verbosity > 0)


@app.command
def check_code_style(verbosity: TyroVerbosityArgType, color: bool = True):
    """
    Check code style by calling darker + flake8
    """
    code_style.check(package_root=get_project_root(), darker_color=color, darker_verbose=verbosity > 0)
