from django.urls import path, include

from rest_framework.routers import SimpleRouter

from .views import (
    TrainingViewSet,
    TrainingApplicationViewSet,
    TrainingsFormViewSet,
)

router = SimpleRouter()
router.register("trainings", TrainingViewSet, basename="training")
router.register("applications", TrainingApplicationViewSet, basename="application")
router.register("forms", TrainingsFormViewSet, basename="form")

urlpatterns = [
    path("", include(router.urls)),
]
