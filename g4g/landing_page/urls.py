from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import LandingPageViewSet, LandingPageStatisticView

router = SimpleRouter()
router.register('landing_page', LandingPageViewSet, basename='landing_page')

urlpatterns = [
    path('', include(router.urls)),
    path('stats/', LandingPageStatisticView.as_view(), name='landing_page_stats')

]
