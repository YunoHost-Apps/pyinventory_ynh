#!/usr/bin/env python3

"""
    Start PyInventory in YunoHost setup locally.
    Note:
        You can only run this script, if you are in a activated PyInventory venv!
    see README for details ;)
"""

import os
import shlex
import subprocess
import sys
from pathlib import Path

os.environ['DJANGO_SETTINGS_MODULE'] = 'ynh_pyinventory_settings'

try:
    import inventory_project  # noqa
except ImportError as err:
    raise ImportError(
        'Couldn\'t import PyInventory. Did you '
        'forget to activate a virtual environment?'
    ) from err


BASE_PATH = Path(__file__).parent.absolute()
TEST_PATH = BASE_PATH / 'local_test'
CONF_PATH = BASE_PATH / 'conf'

FINAL_HOME_PATH = TEST_PATH / 'opt_yunohost'
FINAL_WWW_PATH = TEST_PATH / 'var_www'
LOG_FILE = TEST_PATH / 'var_log_pyinventory.log'

MANAGE_PY_FILE = CONF_PATH / 'manage.py'
CREATE_SUPERUSER_FILE = CONF_PATH / 'create_superuser.py'
SETTINGS_FILE = CONF_PATH / 'ynh_pyinventory_settings.py'
URLS_FILE = CONF_PATH / 'ynh_urls.py'

REPLACES = {
    '__FINAL_HOME_PATH__': str(FINAL_HOME_PATH),
    '__FINAL_WWW_PATH__': str(FINAL_WWW_PATH),
    '__LOG_FILE__': str(TEST_PATH / 'var_log_pyinventory.log'),

    '__PATH_URL__': 'app_path',
    '__DOMAIN__': '127.0.0.1',

    'django.db.backends.postgresql': 'django.db.backends.sqlite3',
    "'NAME': '__APP__',": f"'NAME': '{TEST_PATH / 'test_db.sqlite'}',",

    'django_redis.cache.RedisCache': 'django.core.cache.backends.dummy.DummyCache',

    'DEBUG = False': 'DEBUG = True',

    # Just use the default logging setup from PyInventory project:
    'LOGGING = {': 'HACKED_DEACTIVATED_LOGGING = {',
}


def verbose_check_call(command, verbose=True, **kwargs):
    """ 'verbose' version of subprocess.check_call() """
    if verbose:
        print('_' * 100)
        msg = f'Call: {command!r}'
        verbose_kwargs = ', '.join(f'{k}={v!r}' for k, v in sorted(kwargs.items()))
        if verbose_kwargs:
            msg += f' (kwargs: {verbose_kwargs})'
        print(f'{msg}\n', flush=True)

    env = os.environ.copy()
    env['PYTHONUNBUFFERED'] = '1'

    popenargs = shlex.split(command)
    subprocess.check_call(
        popenargs,
        universal_newlines=True,
        env=env,
        **kwargs
    )


def call_manage_py(args):
    verbose_check_call(
        command=f'{sys.executable} manage.py {args}',
        cwd=FINAL_HOME_PATH,
    )


def copy_patch(src_file, replaces=None):
    dst_file = FINAL_HOME_PATH / src_file.name
    print(f'{src_file.relative_to(BASE_PATH)} -> {dst_file.relative_to(BASE_PATH)}')

    with src_file.open('r') as f:
        content = f.read()

    if replaces:
        for old, new in replaces.items():
            content = content.replace(old, new)

    with dst_file.open('w') as f:
        f.write(content)


def main():
    print('-' * 100)

    assert BASE_PATH.is_dir()
    assert CONF_PATH.is_dir()
    assert SETTINGS_FILE.is_file()
    assert URLS_FILE.is_file()

    for p in (TEST_PATH, FINAL_HOME_PATH, FINAL_WWW_PATH):
        if p.is_dir():
            print(f'Already exists: "{p.relative_to(BASE_PATH)}", ok.')
        else:
            print(f'Create: "{p.relative_to(BASE_PATH)}"')
            p.mkdir(parents=True, exist_ok=True)

    LOG_FILE.touch(exist_ok=True)

    # conf/manage.py -> local_test/manage.py
    copy_patch(src_file=MANAGE_PY_FILE)

    # conf/create_superuser.py -> local_test/opt_yunohost/create_superuser.py
    copy_patch(src_file=CREATE_SUPERUSER_FILE)

    # conf/ynh_pyinventory_settings.py -> local_test/ynh_pyinventory_settings.py
    copy_patch(src_file=SETTINGS_FILE, replaces=REPLACES)

    # conf/ynh_urls.py -> local_test/ynh_urls.py
    copy_patch(src_file=URLS_FILE, replaces=REPLACES)

    with Path(FINAL_HOME_PATH / 'local_settings.py').open('w') as f:
        f.write('# Only for local test run\n')
        f.write('SERVE_FILES=True # used in src/inventory_project/urls.py\n')

    # call "local_test/manage.py" via subprocess:
    call_manage_py('check --deploy')
    call_manage_py('migrate --no-input')
    call_manage_py('collectstatic --no-input')

    verbose_check_call(
        command=f'{sys.executable} create_superuser.py --username="test" --password="test"',
        cwd=FINAL_HOME_PATH,
    )

    try:
        call_manage_py('runserver --nostatic')
    except KeyboardInterrupt:
        print('\nBye ;)')


if __name__ == '__main__':
    main()
