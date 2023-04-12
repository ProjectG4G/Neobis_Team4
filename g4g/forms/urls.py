from django.urls import path

from rest_framework.routers import SimpleRouter

from .views import (
    FormParlerViewSet,
    EventParlerViewSet,
    QuestionViewSet,
    ChoiceViewSet,
    ApplicationViewSet,
    ResponseViewSet,
    EventImageViewSet,
)

router = SimpleRouter()
router.register("events", EventParlerViewSet, basename="event")
router.register("forms", FormParlerViewSet, basename="form")
router.register("questions", QuestionViewSet, basename="question")
router.register("choices", ChoiceViewSet, basename="choice")
router.register("applications", ApplicationViewSet, basename="application")
router.register("responses", ResponseViewSet, basename="response")
router.register("images", EventImageViewSet, basename="eventimage")

urlpatterns = router.urls
