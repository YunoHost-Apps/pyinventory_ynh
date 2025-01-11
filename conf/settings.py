################################################################################
################################################################################

# Please do not modify this file, it will be reset at the next update.
# You can edit the file __DATA_DIR__/local_settings.py and add/modify the settings you need.
# The parameters you add in local_settings.py will overwrite these,
# but you can use the options and documentation in this file to find out what can be done.

################################################################################
################################################################################

from pathlib import Path as __Path

from django_yunohost_integration.base_settings import *  # noqa:F401,F403
from django_yunohost_integration.secret_key import get_or_create_secret as __get_or_create_secret


# https://github.com/jedie/PyInventory
from inventory_project.settings.prod import *  # noqa:F401,F403 isort:skip


from django_yunohost_integration.base_settings import LOGGING  # noqa:F401 isort:skip


DATA_DIR_PATH = __Path('__DATA_DIR__')  # /home/yunohost.app/$app/
assert DATA_DIR_PATH.is_dir(), f'Directory not exists: {DATA_DIR_PATH}'

INSTALL_DIR_PATH = __Path('__INSTALL_DIR__')  # /var/www/$app/
assert INSTALL_DIR_PATH.is_dir(), f'Directory not exists: {INSTALL_DIR_PATH}'

LOG_FILE_PATH = __Path('__LOG_FILE__')  # /var/log/$app/pyinventory_ynh.log
assert LOG_FILE_PATH.is_file(), f'File not exists: {LOG_FILE_PATH}'

PATH_URL = '__PATH__'
PATH_URL = PATH_URL.strip('/')

YNH_CURRENT_HOST = '__YNH_CURRENT_HOST__'  # YunoHost main domain from: /etc/yunohost/current_host

# -----------------------------------------------------------------------------
# config_panel.toml settings:

DEBUG_ENABLED = '__DEBUG_ENABLED__'
DEBUG = DEBUG_ENABLED == '1'

LOG_LEVEL = '__LOG_LEVEL__'
ADMIN_EMAIL = '__ADMIN_EMAIL__'
DEFAULT_FROM_EMAIL = '__DEFAULT_FROM_EMAIL__'


# -----------------------------------------------------------------------------

# Function that will be called to finalize a user profile:
YNH_SETUP_USER = 'setup_user.setup_project_user'


if 'axes' not in INSTALLED_APPS:
    INSTALLED_APPS.append('axes')  # https://github.com/jazzband/django-axes

INSTALLED_APPS.append('django_yunohost_integration.apps.YunohostIntegrationConfig')


SECRET_KEY = __get_or_create_secret(
    DATA_DIR_PATH / 'secret.txt'
)  # /home/yunohost.app/$app/secret.txt


MIDDLEWARE.insert(
    MIDDLEWARE.index('django.contrib.auth.middleware.AuthenticationMiddleware') + 1,
    # login a user via HTTP_REMOTE_USER header from SSOwat:
    'django_yunohost_integration.sso_auth.auth_middleware.SSOwatRemoteUserMiddleware',
)
if 'axes.middleware.AxesMiddleware' not in MIDDLEWARE:
    # AxesMiddleware should be the last middleware:
    MIDDLEWARE.append('axes.middleware.AxesMiddleware')


# Keep ModelBackend around for per-user permissions and superuser
AUTHENTICATION_BACKENDS = (
    'axes.backends.AxesBackend',  # AxesBackend should be the first backend!
    #
    # Authenticate via SSO and nginx 'HTTP_REMOTE_USER' header:
    'django_yunohost_integration.sso_auth.auth_backend.SSOwatUserBackend',
    #
    # Fallback to normal Django model backend:
    'django.contrib.auth.backends.ModelBackend',
)

LOGIN_REDIRECT_URL = None
LOGIN_URL = '/yunohost/sso/'
LOGOUT_REDIRECT_URL = '/yunohost/sso/'
# /yunohost/sso/?action=logout

ROOT_URLCONF = 'urls'  # .../conf/urls.py

# -----------------------------------------------------------------------------


ADMINS = (('__ADMIN__', ADMIN_EMAIL),)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': '__DB_NAME__',
        'USER': '__DB_USER__',
        'PASSWORD': '__DB_PWD__',
        'HOST': '127.0.0.1',
        'PORT': '5432',  # Default Postgres Port
        'CONN_MAX_AGE': 600,
    }
}

# Title of site to use
SITE_TITLE = '__APP__'

# Site domain
SITE_DOMAIN = '__DOMAIN__'

# Subject of emails includes site title
EMAIL_SUBJECT_PREFIX = f'[{SITE_TITLE}] '


# E-mail address that error messages come from.
SERVER_EMAIL = ADMIN_EMAIL

# Default email address to use for various automated correspondence from
# the site managers. Used for registration emails.

# List of URLs your site is supposed to serve
ALLOWED_HOSTS = ['__DOMAIN__']

# _____________________________________________________________________________
# Configuration for caching
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/__REDIS_DB__',
        # If redis is running on same host as PyInventory, you might
        # want to use unix sockets instead:
        # 'LOCATION': 'unix:///var/run/redis/redis.sock?db=1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        },
        'KEY_PREFIX': '__APP__',
    },
}

# _____________________________________________________________________________
# Static files (CSS, JavaScript, Images)

if PATH_URL:
    STATIC_URL = f'/{PATH_URL}/static/'
    MEDIA_URL = f'/{PATH_URL}/media/'
else:
    # Installed to domain root, without a path prefix?
    STATIC_URL = '/static/'
    MEDIA_URL = '/media/'

STATIC_ROOT = str(INSTALL_DIR_PATH / 'static')
MEDIA_ROOT = str(INSTALL_DIR_PATH / 'media')


# _____________________________________________________________________________
# Django-dbbackup

DBBACKUP_STORAGE_OPTIONS['location'] = str(DATA_DIR_PATH / 'backups')

# -----------------------------------------------------------------------------

# Set log file to e.g.: /var/log/$app/$app.log
LOGGING['handlers']['log_file']['filename'] = str(LOG_FILE_PATH)

LOGGING['loggers']['django_yunohost_integration'] = { # TODO: Move to django_yunohost_integration base settings
    'handlers': ['syslog', 'log_file', 'mail_admins'],
    'propagate': False,
}

# Example how to add logging to own app:
LOGGING['loggers']['inventory'] = {
    'handlers': ['syslog', 'log_file', 'mail_admins'],
    'propagate': False,
}
for __logger_name in LOGGING['loggers'].keys():
    LOGGING['loggers'][__logger_name]['level'] = 'DEBUG' if DEBUG else LOG_LEVEL

# -----------------------------------------------------------------------------

try:
    from local_settings import *  # noqa:F401,F403
except ImportError:
    pass
