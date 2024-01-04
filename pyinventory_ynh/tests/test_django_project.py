from unittest.mock import patch

from axes.models import AccessLog
from bx_django_utils.test_utils.html_assertion import assert_html_response_snapshot, HtmlAssertionMixin
from django.conf import LazySettings, settings
from django.contrib.auth.models import User
from django.template.defaulttags import CsrfTokenNode
from django.test import override_settings
from django.test.testcases import TestCase
from django.urls.base import reverse
from django_yunohost_integration.test_utils import generate_basic_auth
from inventory import __version__ as upstream_version

@override_settings(DEBUG=False)
class DjangoYnhTestCase(HtmlAssertionMixin, TestCase):
    def setUp(self):
        super().setUp()

        # Always start a fresh session:
        self.client = self.client_class()

    def test_settings(self):
        assert isinstance(settings, LazySettings)
        assert settings.configured is True

        assert settings.PATH_URL == 'app_path'

        assert str(settings.DATA_DIR_PATH).endswith('/local_test/opt_yunohost'), f'{settings.DATA_DIR_PATH=}'
        assert str(settings.INSTALL_DIR_PATH).endswith('/local_test/var_www'), f'{settings.INSTALL_DIR_PATH=}'
        assert str(settings.LOG_FILE_PATH).endswith(
            '/local_test/var_log_pyinventory.log'
        ), f'{settings.LOG_FILE_PATH=}'

        assert settings.ROOT_URLCONF == 'urls'

    def test_config_panel_settings(self):
        # config_panel.toml settings, set via tests.conftest.pytest_configure():
        assert settings.DEBUG_ENABLED == '0' and settings.DEBUG is False
        assert settings.LOG_LEVEL == 'INFO'
        assert settings.ADMIN_EMAIL == 'foo-bar@test.tld'
        assert settings.DEFAULT_FROM_EMAIL == 'django_app@test.tld'

    def test_auth(self):
        self.assertEqual(settings.PATH_URL, 'app_path')
        self.assertEqual(reverse('admin:index'), '/app_path/')

        # SecurityMiddleware should redirects all non-HTTPS requests to HTTPS:
        assert settings.SECURE_SSL_REDIRECT is True
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
            expected_url='/app_path/login/?next=%2Fapp_path%2F',
            fetch_redirect_response=False,
        )

    def test_create_unknown_user(self):
        assert User.objects.count() == 0

        self.client.cookies['SSOwAuthUser'] = 'test'

        with patch.object(CsrfTokenNode, 'render', return_value='MockedCsrfTokenNode'):
            response = self.client.get(
                path='/app_path/',
                HTTP_REMOTE_USER='test',
                HTTP_AUTH_USER='test',
                HTTP_AUTHORIZATION='basic dGVzdDp0ZXN0MTIz',
                secure=True,
            )

        assert User.objects.count() == 1
        user = User.objects.first()
        assert user.username == 'test'
        assert user.is_active is True
        assert user.is_staff is True  # Set by: conf.setup_user.setup_project_user
        assert user.is_superuser is False

        self.assert_html_parts(
            response,
            parts=(
                f'<h1 id="site-name"><a href="/app_path/">PyInventory v{upstream_version}</a></h1>',
                '<strong>test</strong>',
                #
                # Can create PyInventory model entries:
                '<a class="addlink" href="/app_path/inventory/itemmodel/add/">Add</a>',
                '<a class="addlink" href="/app_path/inventory/locationmodel/add/">Add</a>',
                '<a class="addlink" href="/app_path/inventory/memomodel/add/">Add</a>',
            ),
        )
        assert_html_response_snapshot(response, query_selector='#main', validate=False)

    def test_wrong_auth_user(self):
        assert User.objects.count() == 0
        assert AccessLog.objects.count() == 0

        self.client.cookies['SSOwAuthUser'] = 'test'

        response = self.client.get(
            path='/app_path/admin/',
            HTTP_REMOTE_USER='test',
            HTTP_AUTH_USER='foobar',  # <<< wrong user name
            HTTP_AUTHORIZATION='basic dGVzdDp0ZXN0MTIz',
            secure=True,
        )

        assert User.objects.count() == 1
        user = User.objects.first()
        assert user.username == 'test'
        assert user.is_active is True
        assert user.is_staff is True  # Set by: conf.setup_user.setup_project_user
        assert user.is_superuser is False

        assert AccessLog.objects.count() == 1

        assert response.status_code == 403  # Forbidden

    def test_wrong_cookie(self):
        assert User.objects.count() == 0
        assert AccessLog.objects.count() == 0

        self.client.cookies['SSOwAuthUser'] = 'foobar'  # <<< wrong user name

        response = self.client.get(
            path='/app_path/',
            HTTP_REMOTE_USER='test',
            HTTP_AUTH_USER='test',
            HTTP_AUTHORIZATION='basic dGVzdDp0ZXN0MTIz',
            secure=True,
        )

        assert User.objects.count() == 1
        user = User.objects.first()
        assert user.username == 'test'
        assert user.is_active is True
        assert user.is_staff is True  # Set by: conf.setup_user.setup_project_user
        assert user.is_superuser is False

        assert AccessLog.objects.count() == 1

        assert response.status_code == 403  # Forbidden

    def test_wrong_authorization_user(self):
        assert User.objects.count() == 0

        self.client.cookies['SSOwAuthUser'] = 'test'

        response = self.client.get(
            path='/app_path/',
            HTTP_REMOTE_USER='test',
            HTTP_AUTH_USER='test',
            HTTP_AUTHORIZATION=generate_basic_auth(
                username='foobar',  # <<< wrong user name
                password='test123',
            ),
            secure=True,
        )

        assert User.objects.count() == 1
        user = User.objects.first()
        assert user.username == 'test'
        assert user.is_active is True
        assert user.is_staff is True  # Set by: conf.setup_user.setup_project_user
        assert user.is_superuser is False

        assert AccessLog.objects.count() == 1

        assert response.status_code == 403  # Forbidden
