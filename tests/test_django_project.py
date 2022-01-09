from pathlib import Path

from axes.models import AccessLog
from bx_django_utils.test_utils.html_assertion import HtmlAssertionMixin
from django.conf import LazySettings, settings
from django.contrib.auth.models import User
from django.test import override_settings
from django.test.testcases import TestCase
from django.urls import NoReverseMatch
from django.urls.base import reverse
from django_yunohost_integration.test_utils import generate_basic_auth
from django_yunohost_integration.views import request_media_debug_view

import inventory


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

        def assert_path(path, end_text):
            assert isinstance(path, Path)
            path = str(path)
            assert path.endswith(end_text)

        assert_path(settings.FINAL_HOME_PATH, '/local_test/opt_yunohost')
        assert_path(settings.FINAL_WWW_PATH, '/local_test/var_www')
        assert_path(settings.LOG_FILE, '/local_test/var_log_pyinventory.log')

        assert settings.ROOT_URLCONF == 'urls'

    def test_urls(self):
        assert reverse('admin:index') == '/app_path/'

        # The django_yunohost_integration debug view should not be available:
        with self.assertRaises(NoReverseMatch):
            reverse(request_media_debug_view)

        # Serve user uploads via django_tools.serve_media_app:
        assert settings.MEDIA_URL == '/app_path/media/'
        assert reverse('serve_media_app:serve-media', kwargs={'user_token': 'token', 'path': 'foo/bar/'}) == (
            '/app_path/media/token/foo/bar/'
        )

    def test_auth(self):
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
        self.assertRedirects(response, expected_url='/app_path/login/?next=/app_path/', fetch_redirect_response=False)

    @override_settings(SECURE_SSL_REDIRECT=False)
    def test_create_unknown_user(self):
        assert User.objects.count() == 0

        self.client.cookies['SSOwAuthUser'] = 'test'

        response = self.client.get(
            path='/app_path/',
            HTTP_REMOTE_USER='test',
            HTTP_AUTH_USER='test',
            HTTP_AUTHORIZATION='basic dGVzdDp0ZXN0MTIz',
        )

        assert User.objects.count() == 1
        user = User.objects.first()
        assert user.username == 'test'
        assert user.is_active is True
        assert user.is_staff is True  # Set by: django_yunohost_integration
        assert user.is_superuser is False

        assert response.status_code == 200
        self.assert_html_parts(
            response,
            parts=(
                f'<title>Site administration | PyInventory v{inventory.__version__}</title>',
                '<strong>test</strong>',
            ),
        )

    @override_settings(SECURE_SSL_REDIRECT=False)
    def test_wrong_auth_user(self):
        assert User.objects.count() == 0
        assert AccessLog.objects.count() == 0

        self.client.cookies['SSOwAuthUser'] = 'test'

        response = self.client.get(
            path='/app_path/',
            HTTP_REMOTE_USER='test',
            HTTP_AUTH_USER='foobar',  # <<< wrong user name
            HTTP_AUTHORIZATION='basic dGVzdDp0ZXN0MTIz',
        )

        assert User.objects.count() == 1
        user = User.objects.first()
        assert user.username == 'test'
        assert user.is_active is True
        assert user.is_staff is True  # Set by: django_yunohost_integration
        assert user.is_superuser is False

        assert AccessLog.objects.count() == 1

        assert response.status_code == 403  # Forbidden

    @override_settings(SECURE_SSL_REDIRECT=False)
    def test_wrong_cookie(self):
        assert User.objects.count() == 0
        assert AccessLog.objects.count() == 0

        self.client.cookies['SSOwAuthUser'] = 'foobar'  # <<< wrong user name

        response = self.client.get(
            path='/app_path/',
            HTTP_REMOTE_USER='test',
            HTTP_AUTH_USER='test',
            HTTP_AUTHORIZATION='basic dGVzdDp0ZXN0MTIz',
        )

        assert User.objects.count() == 1
        user = User.objects.first()
        assert user.username == 'test'
        assert user.is_active is True
        assert user.is_staff is True  # Set by: django_yunohost_integration
        assert user.is_superuser is False

        assert AccessLog.objects.count() == 1

        assert response.status_code == 403  # Forbidden

    @override_settings(SECURE_SSL_REDIRECT=False)
    def test_wrong_authorization_user(self):
        assert User.objects.count() == 0

        self.client.cookies['SSOwAuthUser'] = 'test'

        response = self.client.get(
            path='/app_path/',
            HTTP_REMOTE_USER='test',
            HTTP_AUTH_USER='test',
            HTTP_AUTHORIZATION=generate_basic_auth(username='foobar', password='test123'),  # <<< wrong user name
        )

        assert User.objects.count() == 1
        user = User.objects.first()
        assert user.username == 'test'
        assert user.is_active is True
        assert user.is_staff is True  # Set by: django_yunohost_integration
        assert user.is_superuser is False

        assert AccessLog.objects.count() == 1

        assert response.status_code == 403  # Forbidden
