from django.conf import settings
from django.conf.urls import include, static
from django.contrib import admin
from django.urls import path


# def debug_view(request):
#     """ debug request.META """
#     if not request.user.is_authenticated:
#         from django.shortcuts import redirect
#         return redirect('admin:index')
#
#     import pprint
#     meta = pprint.pformat(request.META)
#     html = f'<html><body>request.META: <pre>{meta}</pre></body></html>'
#     from django.http import HttpResponse
#     return HttpResponse(html)


if settings.PATH_URL:
    # settings.PATH_URL is the $YNH_APP_ARG_PATH
    # Prefix all urls with "PATH_URL":
    urlpatterns = [
        # path(f'{settings.PATH_URL}/debug/', debug_view),
        path(f'{settings.PATH_URL}/', admin.site.urls),

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
