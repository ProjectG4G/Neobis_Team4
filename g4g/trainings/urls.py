from django.urls import path, include

from rest_framework.routers import SimpleRouter

from .views import (
    TrainingViewSet,
    TrainingApplicationViewSet,
    TrainingsFormViewSet,
    TrainingApplicantViewSet,
)

router = SimpleRouter()
router.register("trainings", TrainingViewSet, basename="training")
router.register(
    "applications", TrainingApplicationViewSet, basename="training-application"
)
router.register("applicants", TrainingApplicantViewSet, basename="applicant")
router.register("forms", TrainingsFormViewSet, basename="training-form")

urlpatterns = [
    path("", include(router.urls)),
]
