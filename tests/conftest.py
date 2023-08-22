"""
    Special pytest init:

        - Build a "local_test" YunoHost installation
        - init Django with this local test installation

    So the pytests will run against this local test installation
"""
import os
import sys
from pathlib import Path

import django
from django_yunohost_integration.local_test import CreateResults, create_local_test


BASE_PATH = Path(__file__).parent.parent

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'


def pytest_configure():
    print('Compile YunoHost files...')
    result: CreateResults = create_local_test(
        django_settings_path=BASE_PATH / 'conf' / 'settings.py',
        destination=BASE_PATH / 'local_test',
        runserver=False,
        extra_replacements={
            '__DEBUG_ENABLED__': 'NO',  # "YES" or "NO" string
            '__LOG_LEVEL__': 'INFO',
            '__ADMIN_EMAIL__': 'foo-bar@test.tld',
            '__DEFAULT_FROM_EMAIL__': 'django_app@test.tld',
        },
    )
    print('Local test files created:')
    print(result)

    os.chdir(result.data_dir_path)
    data_dir = str(result.data_dir_path)
    if data_dir not in sys.path:
        sys.path.insert(0, data_dir)

    django.setup()
