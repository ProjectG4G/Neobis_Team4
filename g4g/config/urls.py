from django.contrib import admin
from django.urls import path, include

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("users.urls")),
    path("api/news/", include("news.urls")),
    path("api/rest_auth/", include("rest_framework.urls")),
    path("api/mentorship/", include("mentorship.urls")),
    path("api/trainings/", include("trainings.urls")),
    path("geoapi/", include("geoapi.urls")),
    path("api/", include("landing_page.urls")),
    path("api/", include("forms.urls")),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    # Optional UI:
    path(
        "api/swagger/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]
