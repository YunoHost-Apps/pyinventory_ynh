from django.conf import settings
from django.conf.urls import include
from django.contrib import admin
from django.urls import path


if settings.PATH_URL:
    # settings.PATH_URL is __PATH__
    # Prefix all urls with "PATH_URL":
    urlpatterns = [
        # MEDIA_URL contains the "PATH_URL" already:
        path(settings.MEDIA_URL.lstrip('/'), include('django_tools.serve_media_app.urls')),
        path(f'{settings.PATH_URL}/', admin.site.urls),
        path(f'{settings.PATH_URL}/tinymce/', include('tinymce.urls')),
    ]
else:
    # Installed to domain root, without a path prefix
    # Just use the default project urls.py
    from inventory_project.urls import urlpatterns  # noqa
