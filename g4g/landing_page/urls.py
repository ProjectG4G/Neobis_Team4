from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import LandingPageViewSet

router = SimpleRouter()
router.register('landing_page', LandingPageViewSet, basename='landing_page')

urlpatterns = [
    path('', include(router.urls)),
]
