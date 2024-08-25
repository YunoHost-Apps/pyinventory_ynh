#!.venv/bin/python3

"""
    Call the "manage.py" from the local test environment.
"""

from django_yunohost_integration.local_test import run_local_test_manage


if __name__ == '__main__':
    run_local_test_manage()
