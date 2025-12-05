
from pyinventory_ynh.cli_dev import app
from pyinventory_ynh.tests import create_local_test_files


@app.command
def local_test():
    """
    Build a "local_test" YunoHost installation and start the Django dev. server against it.
    """
    create_local_test_files(runserver=True)
