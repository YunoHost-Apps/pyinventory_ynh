"""
https://github.com/jedie/manageprojects/blob/main/docs/install_python.md#include-in-own-projects
"""

from django_yunohost_integration.path_utils import get_project_root
from manageprojects.utilities.include_install_python import IncludeInstallPythonBaseTestCase


class IncludeInstallPythonTestCase(IncludeInstallPythonBaseTestCase):
    """
    Updates `conf/install_python.py` from `manageprojects` if needed.
    """

    DESTINATION_PATH = get_project_root() / 'conf' / 'install_python.py'

    def test_install_python_is_up2date(self):
        self.auto_update_install_python()
