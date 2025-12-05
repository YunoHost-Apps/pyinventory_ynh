from axes.models import AccessLog
from bx_django_utils.test_utils.html_assertion import HtmlAssertionMixin
from django.conf import LazySettings, settings
from django.contrib.auth.models import User
from django.test import override_settings
from django.test.testcases import TestCase
from django.urls.base import reverse
from django.views.generic import RedirectView
from django_yunohost_integration.test_utils import generate_basic_auth
from django_yunohost_integration.yunohost.tests.test_ynh_jwt import create_jwt
from inventory import __version__ as upstream_version


class DjangoYnhTestCase(HtmlAssertionMixin, TestCase):
    maxDiff = None

    def setUp(self):
        super().setUp()

        # Always start a fresh session:
        self.client = self.client_class()

    def test_settings(self):
        self.assertIsInstance(settings, LazySettings)
        self.assertIs(settings.configured, True)

        # default YunoHost app replacements:

        self.assertTrue(
            str(settings.DATA_DIR_PATH).endswith('/local_test/opt_yunohost'),
            msg=f'{settings.DATA_DIR_PATH=}',
        )
        self.assertTrue(
            str(settings.INSTALL_DIR_PATH).endswith('/local_test/var_www'),
            msg=f'{settings.INSTALL_DIR_PATH=}',
        )
        self.assertTrue(
            str(settings.LOG_FILE_PATH).endswith('/local_test/var_log_pyinventory.log'),
            msg=f'{settings.LOG_FILE_PATH=}',
        )
        self.assertEqual(settings.PATH_URL, 'app_path')
        self.assertEqual(settings.MEDIA_URL, '/app_path/media/')
        self.assertEqual(settings.STATIC_URL, '/app_path/static/')

        # config_panel.toml settings:

        self.assertEqual(settings.DEBUG_ENABLED, '1')
        self.assertEqual(settings.LOG_LEVEL, 'DEBUG')
        self.assertEqual(settings.ADMIN_EMAIL, 'foo-bar@test.tld')
        self.assertEqual(settings.DEFAULT_FROM_EMAIL, 'django_app@test.tld')

        # Normal settings:
        self.assertIs(settings.DEBUG, False)
        self.assertEqual(settings.ROOT_URLCONF, 'urls')
        self.assertEqual(settings.ADMINS, (('The Admin Username', 'foo-bar@test.tld'),))
        self.assertEqual(settings.MANAGERS, (('The Admin Username', 'foo-bar@test.tld'),))
        self.assertEqual(settings.SERVER_EMAIL, 'foo-bar@test.tld')
        self.assertEqual(
            settings.ALLOWED_HOSTS,
            ['127.0.0.1', 'testserver'],  # Added by Django's setup_test_environment()
        )

        # Logging example correct?
        log_filename = settings.LOGGING['handlers']['log_file']['filename']
        self.assertTrue(log_filename.endswith('/local_test/var_log_pyinventory.log'), log_filename)
        self.assertEqual(
            settings.LOGGING['loggers']['django_yunohost_integration'],
            {
                'handlers': ['log_file', 'mail_admins'],
                'level': 'DEBUG',
                'propagate': False,
            },
        )

    def test_urls(self):
        self.assertEqual(settings.PATH_URL, 'app_path')
        self.assertEqual(settings.ROOT_URLCONF, 'urls')
        self.assertEqual(settings.LOGIN_URL, 'ssowat-login')
        self.assertEqual(reverse('admin:index'), '/app_path/')  # Location of PyInventory ;)
        self.assertEqual(reverse('ssowat-login'), '/app_path/sso-login/')

        # After login redirected to app root path:
        self.assertEqual(settings.LOGIN_REDIRECT_URL, '/app_path/')

        #########################################################################################
        # non-HTTPS request should be redirected to HTTPS:
        self.assertIs(settings.SECURE_SSL_REDIRECT, True)
        response = self.client.get('/', secure=True)
        self.assertEqual(response.resolver_match.func.view_class, RedirectView)
        self.assertRedirects(response, expected_url='/app_path/', fetch_redirect_response=False)

    def test_auth(self):
        # SecurityMiddleware should redirects all non-HTTPS requests to HTTPS:
        self.assertIs(settings.SECURE_SSL_REDIRECT, True)
        response = self.client.get('/app_path/', secure=False)
        self.assertRedirects(
            response,
            status_code=301,  # permanent redirect
            expected_url='https://testserver/app_path/',
            fetch_redirect_response=False,
        )

        response = self.client.get('/app_path/', secure=True)
        self.assertRedirects(
            response,
            expected_url='/app_path/login/?next=/app_path/',
            fetch_redirect_response=False,
        )

    @override_settings(SECURE_SSL_REDIRECT=False)
    def test_login_happy_path(self):
        self.assertEqual(User.objects.count(), 0)

        self.client.cookies['yunohost.portal'] = create_jwt(username='Mr. Test User')
        auth_string = generate_basic_auth(username='Mr. Test User', password='foo bar')
        with self.assertLogs('django_yunohost_integration') as logs:
            response = self.client.get(
                path='/app_path/',
                HTTP_YNH_USER='Mr. Test User',
                HTTP_AUTH_USER='Mr. Test User',
                HTTP_AUTHORIZATION=auth_string,
            )
        try:
            self.assertEqual(User.objects.count(), 1)
            user = User.objects.first()
            self.assertEqual(user.username, 'Mr. Test User')
            self.assertIs(user.is_active, True)
            self.assertIs(user.is_staff, True)  # Set by: 'setup_user.setup_project_user'

            # Our conf/setup_user.py does not set is_superuser=False
            self.assertIs(user.is_superuser, False)
            # Our conf/setup_user.py adds the user to the 'normal user' group:
            self.assertEqual(list(user.groups.values_list('name', flat=True)), ['normal user'])
        except AssertionError as err:
            raise AssertionError('Log: ' + '\n'.join(logs.output)) from err

        self.assert_html_parts(
            response,
            parts=(
                f'<title>Site administration | PyInventory v{upstream_version}</title>',
                '<h1>Site administration</h1>',
                (
                    '<a href="/app_path/"><img src="/app_path/static/PyInventory_Logo.svg" alt="Logo">'
                    f'PyInventory v{upstream_version}</a>'
                ),
                '<strong>Mr. Test User</strong>',
                '<a href="/app_path/inventory/itemmodel/">Items</a>',
            ),
        )
        self.assertEqual(
            logs.output,
            [
                "INFO:django_yunohost_integration.sso_auth.auth_backend:Remote user authenticate: 'Mr. Test User'",
                'WARNING:django_yunohost_integration.sso_auth.auth_backend:Configure user Mr. Test User',
                'WARNING:django_yunohost_integration.sso_auth.auth_backend:Remote user login: Mr. Test User',
                "INFO:django_yunohost_integration.yunohost.ynh_jwt:JWT username 'Mr. Test User' is valid",
                'INFO:django_yunohost_integration.sso_auth.auth_middleware:Remote user "Mr. Test User" was logged in',
            ],
        )

    @override_settings(SECURE_SSL_REDIRECT=False)
    def test_wrong_cookie(self):
        self.assertEqual(User.objects.count(), 0)
        self.assertEqual(AccessLog.objects.count(), 0)

        self.client.cookies['yunohost.portal'] = create_jwt(username='foobar')  # <<< wrong user name

        with self.assertLogs('django_yunohost_integration') as logs:
            response = self.client.get(
                path='/app_path/',
                HTTP_YNH_USER='test',
                HTTP_AUTH_USER='test',
                HTTP_AUTHORIZATION='basic dGVzdDp0ZXN0MTIz',
            )

        try:
            self.assertEqual(User.objects.count(), 1)
            user = User.objects.first()
            self.assertEqual(user.username, 'test')
            self.assertIs(user.is_active, True)
            self.assertIs(user.is_staff, True)  # Set by: 'setup_user.setup_project_user'

            # Our conf/setup_user.py does not set is_superuser=False
            self.assertIs(user.is_superuser, False)
            # Our conf/setup_user.py adds the user to the 'normal user' group:
            self.assertEqual(list(user.groups.values_list('name', flat=True)), ['normal user'])

            self.assertEqual(AccessLog.objects.count(), 1)

            self.assertEqual(response.status_code, 400)  # Bad Request
        except AssertionError as err:
            raise AssertionError('Log: ' + '\n'.join(logs.output)) from err
        self.assertEqual(
            logs.output,
            [
                "INFO:django_yunohost_integration.sso_auth.auth_backend:Remote user authenticate: 'test'",
                'WARNING:django_yunohost_integration.sso_auth.auth_backend:Configure user test',
                'WARNING:django_yunohost_integration.sso_auth.auth_backend:Remote user login: test',
                (
                    "ERROR:django_yunohost_integration.yunohost.ynh_jwt:"
                    "Mismatch: jwt_username='foobar' is not user.username='test'"  # <<< wrong user name
                ),
            ],
        )

    @override_settings(SECURE_SSL_REDIRECT=False)
    def test_wrong_authorization_user(self):
        self.assertEqual(User.objects.count(), 0)
        self.assertEqual(AccessLog.objects.count(), 0)

        self.client.cookies['yunohost.portal'] = create_jwt(username='test')

        with self.assertLogs('django_yunohost_integration') as logs:
            response = self.client.get(
                path='/app_path/',
                HTTP_YNH_USER='test',
                HTTP_AUTH_USER='test',
                HTTP_AUTHORIZATION=generate_basic_auth(username='foobar', password='test123'),  # <<< wrong user name
            )
        try:
            self.assertEqual(User.objects.count(), 1)
            user = User.objects.first()
            self.assertEqual(user.username, 'test')
            self.assertIs(user.is_active, True)
            self.assertIs(user.is_staff, True)  # Set by: 'setup_user.setup_project_user'

            # Our conf/setup_user.py does not set is_superuser=False
            self.assertIs(user.is_superuser, False)
            # Our conf/setup_user.py adds the user to the 'normal user' group:
            self.assertEqual(list(user.groups.values_list('name', flat=True)), ['normal user'])

            self.assertEqual(AccessLog.objects.count(), 1)

            self.assertEqual(response.status_code, 403)  # Forbidden
        except AssertionError as err:
            raise AssertionError('Log: ' + '\n'.join(logs.output)) from err
        self.assertEqual(
            logs.output,
            [
                "INFO:django_yunohost_integration.sso_auth.auth_backend:Remote user authenticate: 'test'",
                'WARNING:django_yunohost_integration.sso_auth.auth_backend:Configure user test',
                'WARNING:django_yunohost_integration.sso_auth.auth_backend:Remote user login: test',
                "INFO:django_yunohost_integration.yunohost.ynh_jwt:JWT username 'test' is valid",
                (
                    "ERROR:django_yunohost_integration.sso_auth.auth_middleware:"
                    "'HTTP_AUTHORIZATION' mismatch: username='foobar' is not test"  # <<< wrong user name
                ),
            ],
        )
