from django.contrib import admin
from django.urls import path, include
from django_api_admin.sites import site

from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/admin/', site.urls),
    path('api/auth/', include('users.urls')),
    path('api/rest_auth/', include('rest_framework.urls')),
    path('geoapi/', include('geoapi.urls')),

    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('api/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
