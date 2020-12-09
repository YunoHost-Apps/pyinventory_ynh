from django.conf import settings
from django.conf.urls import include
from django.urls import path

# settings.PATH_URL is the $YNH_APP_ARG_PATH
if settings.PATH_URL:
    urlpatterns = [
        # XXX: Hack - the MEDIA_URL contains the "PATH_URL" already:
        path(settings.MEDIA_URL.lstrip('/'), include('django_tools.serve_media_app.urls')),

        # Prefix all urls with "PATH_URL":
        path(f'{settings.PATH_URL}/', include('inventory_project.urls'))
    ]
else:
    # Installed to domain root, without a path prefix?
    from inventory_project.urls import urlpatterns  # noqa
