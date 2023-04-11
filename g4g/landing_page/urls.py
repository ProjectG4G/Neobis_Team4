from django.urls import path
from .views import LandingPageStatisticView


urlpatterns = [
    path(
        "landing_page/stats/",
        LandingPageStatisticView.as_view(),
        name="landing_page_stats",
    )
]
