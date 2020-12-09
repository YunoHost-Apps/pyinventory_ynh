from django.conf.urls import include
from django.urls import path

urlpatterns = [
    path('__PATH_URL__/', include('inventory_project.urls'))
]