from django.contrib import admin
from django.urls import path, include, re_path

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/rest_auth/", include("rest_framework.urls")),
    path("geoapi/", include("geoapi.urls")),
    path("api/auth/", include("users.urls")),
    path("api/forms/", include("forms.urls")),
    path("api/mentorship/", include("mentorship.urls")),
    path("api/training/", include("trainings.urls")),
    path("api/shop/", include("products.urls")),
    path("api/news/", include("news.urls")),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/", include("landing_page.urls")),
    # Optional UI:
    path(
        "api/swagger/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]
