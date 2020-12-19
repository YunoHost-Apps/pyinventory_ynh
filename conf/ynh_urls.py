from django.conf import settings
from django.conf.urls import include, static
from django.contrib import admin
from django.urls import path
from django.views.generic import RedirectView

# settings.PATH_URL is the $YNH_APP_ARG_PATH
if settings.PATH_URL:
    # Prefix all urls with "PATH_URL":
    urlpatterns = [
        path(f'{settings.PATH_URL}/admin/', admin.site.urls),

        path(f'{settings.PATH_URL}/', RedirectView.as_view(pattern_name='admin:index')),

        path(f'{settings.PATH_URL}/ckeditor/', include('ckeditor_uploader.urls')),

        # MEDIA_URL contains the "PATH_URL" already:
        path(settings.MEDIA_URL.lstrip('/'), include('django_tools.serve_media_app.urls')),
    ]
    if settings.SERVE_FILES:
        urlpatterns += static.static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
else:
    # Installed to domain root, without a path prefix
    # Just use the default project urls.py
    from inventory_project.urls import urlpatterns  # noqa
