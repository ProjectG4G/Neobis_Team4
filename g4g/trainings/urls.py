from django.urls import path, include

from rest_framework.routers import SimpleRouter

from .views import TrainingViewSet, TrainingApplicationViewSet

router = SimpleRouter()
router.register("trainings", TrainingViewSet, basename="training")
router.register("applications", TrainingApplicationViewSet, basename="applications")

urlpatterns = [
    path("", include(router.urls)),
]
