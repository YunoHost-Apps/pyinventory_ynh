from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView
from django_yunohost_integration.yunohost_utils import SSOwatLoginRedirectView


if settings.PATH_URL:
    # settings.PATH_URL is __PATH__
    # Prefix all urls with "PATH_URL":
    urlpatterns = [
        path('', RedirectView.as_view(url=f'{settings.PATH_URL}/')),
        # MEDIA_URL contains the "PATH_URL" already:
        path(settings.MEDIA_URL.lstrip('/'), include('django_tools.serve_media_app.urls')),
        path(f'{settings.PATH_URL}/', admin.site.urls),
        path(f'{settings.PATH_URL}/tinymce/', include('tinymce.urls')),
        #
        # Cover over the default Django Admin Login with SSOWat login:
        path(f'{settings.PATH_URL}/sso-login/', SSOwatLoginRedirectView.as_view(), name='ssowat-login'),
    ]
else:
    # Installed to domain root, without a path prefix
    # Just use the default project urls.py
    from inventory_project.urls import urlpatterns  # noqa

    urlpatterns = [
        path('admin/sso-login/', SSOwatLoginRedirectView.as_view(), name='ssowat-login'),
        *urlpatterns
    ]
