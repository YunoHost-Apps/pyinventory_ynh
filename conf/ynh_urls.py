from django.conf import settings
from django.conf.urls import include
from django.urls import path

# settings.PATH_URL is the $YNH_APP_ARG_PATH
if settings.PATH_URL:
    urlpatterns = [
        path(f'{settings.PATH_URL}/', include('inventory_project.urls'))
    ]
else:
    # Installed to domain root, without a path prefix?
    from inventory_project.urls import urlpatterns  # noqa
