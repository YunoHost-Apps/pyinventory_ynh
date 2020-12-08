################################################################################
################################################################################

# Please do not modify this file, it will be reset at the next update.
# You can edit the file __FINAL_HOME_PATH__/local_settings.py and add/modify the settings you need.
# The parameters you add in local_settings.py will overwrite these,
# but you can use the options and documentation in this file to find out what can be done.

################################################################################
################################################################################

from pathlib import Path as __Path

from inventory_project.settings.base import *  # noqa

DEBUG = False

# -----------------------------------------------------------------------------

FINAL_HOME_PATH = __Path('__FINAL_HOME_PATH__')
assert FINAL_HOME_PATH.is_dir(), f'Directory not exists: {FINAL_HOME_PATH}'

FINAL_WWW_PATH = __Path('__FINAL_WWW_PATH__')
assert FINAL_WWW_PATH.is_dir(), f'Directory not exists: {FINAL_WWW_PATH}'

LOG_FILE = __Path('__LOG_FILE__')
assert LOG_FILE.is_file(), f'File not exists: {LOG_FILE}'

# -----------------------------------------------------------------------------

ADMINS = (
    ('__ADMIN__', '__ADMINMAIL__'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': '__APP__',
        'USER': '__APP__',
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
SERVER_EMAIL = 'noreply@__DOMAIN__'

# Default email address to use for various automated correspondence from
# the site managers. Used for registration emails.
DEFAULT_FROM_EMAIL = '__ADMINMAIL__'

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
            'PARSER_CLASS': 'redis.connection.HiredisParser',
            'PASSWORD': None,
            'CONNECTION_POOL_KWARGS': {},
        },
        'KEY_PREFIX': '__APP__',
    },
}

# _____________________________________________________________________________
# Static files (CSS, JavaScript, Images)

STATIC_URL = '/static/'
STATIC_ROOT = str(FINAL_WWW_PATH / 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = str(FINAL_WWW_PATH / 'media')

# -----------------------------------------------------------------------------

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '{asctime} {levelname} {name} {module}.{funcName} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'formatter': 'verbose',
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
        },
        'syslog': {
            'level': 'DEBUG',
            'class': 'logging.handlers.WatchedFileHandler',
            'formatter': 'verbose',
            'filename': str(LOG_FILE),
        },
    },
    'loggers': {
        '': {'handlers': ['syslog', 'mail_admins'], 'level': 'INFO', 'propagate': False},
        'django': {'handlers': ['syslog', 'mail_admins'], 'level': 'INFO', 'propagate': False},
        'axes': {'handlers': ['syslog', 'mail_admins'], 'level': 'WARNING', 'propagate': False},
        'django_tools': {'handlers': ['syslog', 'mail_admins'], 'level': 'INFO', 'propagate': False},
        'inventory': {'handlers': ['syslog', 'mail_admins'], 'level': 'INFO', 'propagate': False},
    },
}

# -----------------------------------------------------------------------------

try:
    from .local_settings import *  # noqa
except ImportError:
    pass
