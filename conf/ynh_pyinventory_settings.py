################################################################################
################################################################################

# Please do not modify this file, it will be reset at the next update.
# You can edit the file __FINAL_HOME_PATH__/local_settings.py and add/modify the settings you need.
# The parameters you add in local_settings.py will overwrite these,
# but you can use the options and documentation in this file to find out what can be done.

################################################################################
################################################################################

from pathlib import Path as __Path

import ldap
from django_auth_ldap.config import LDAPSearch
from inventory_project.settings.base import *  # noqa

DEBUG = False

# -----------------------------------------------------------------------------

FINAL_HOME_PATH = __Path('__FINAL_HOME_PATH__')  # /opt/yunohost/$app
assert FINAL_HOME_PATH.is_dir(), f'Directory not exists: {FINAL_HOME_PATH}'

FINAL_WWW_PATH = __Path('__FINAL_WWW_PATH__')  # /var/www/$app
assert FINAL_WWW_PATH.is_dir(), f'Directory not exists: {FINAL_WWW_PATH}'

LOG_FILE = __Path('__LOG_FILE__')  # /var/log/$app/pyinventory.log
assert LOG_FILE.is_file(), f'File not exists: {LOG_FILE}'

PATH_URL = '__PATH_URL__'  # $YNH_APP_ARG_PATH
PATH_URL = PATH_URL.strip('/')

# -----------------------------------------------------------------------------

ROOT_URLCONF = 'ynh_urls'  # /opt/yunohost/pyinventory/ynh_urls.py

# -----------------------------------------------------------------------------
# https://github.com/django-auth-ldap/django-auth-ldap

LDAP_SERVER_URI = 'ldap://localhost:389'
LDAP_START_TLS = True

# enable anonymous searches
# https://django-auth-ldap.readthedocs.io/en/latest/authentication.html?highlight=anonymous#search-bind
LDAP_BIND_DN = ''
LDAP_BIND_PASSWORD = ''

LDAP_ROOT_DN = 'ou=users,dc=yunohost,dc=org'

AUTH_LDAP_USER_SEARCH = LDAPSearch(LDAP_ROOT_DN, ldap.SCOPE_SUBTREE, '(uid=%(user)s)')

# Populate the Django user from the LDAP directory.
AUTH_LDAP_USER_ATTR_MAP = {
    'username': 'uid',
    'first_name': 'givenName',
    'last_name': 'sn',
    'email': 'mail',
}

# This is the default, but I like to be explicit.
AUTH_LDAP_ALWAYS_UPDATE_USER = True

# Use LDAP group membership to calculate group permissions.
AUTH_LDAP_FIND_GROUP_PERMS = True

# Cache distinguished names and group memberships for an hour to minimize LDAP traffic
AUTH_LDAP_CACHE_TIMEOUT = 3600

# Keep ModelBackend around for per-user permissions and superuser
AUTHENTICATION_BACKENDS = (
    'django_auth_ldap.backend.LDAPBackend',
    'django.contrib.auth.backends.ModelBackend',
)

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

STATIC_ROOT = str(FINAL_WWW_PATH / 'static')
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
        'django_auth_ldap': {'handlers': ['syslog', 'mail_admins'], 'level': 'DEBUG', 'propagate': False},
        'inventory': {'handlers': ['syslog', 'mail_admins'], 'level': 'INFO', 'propagate': False},
    },
}

# -----------------------------------------------------------------------------

try:
    from .local_settings import *  # noqa
except ImportError:
    pass
