from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views import TrainingsParlerViewSet

router = SimpleRouter()
router.register("trainings", TrainingsParlerViewSet, basename="training")

urlpatterns = [
    path("", include(router.urls)),
]
