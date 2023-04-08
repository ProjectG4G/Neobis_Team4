from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import (
    MentorshipViewSet,
    ApplicationsViewSet,
    FeedbackViewSet,
    FAQViewSet,
    QuestionsViewSet,
    MentorProfileViewSet,
)

router = SimpleRouter()
router.register("programs", MentorshipViewSet, basename="program")
router.register("questions", QuestionsViewSet, basename="question")
router.register("applications", ApplicationsViewSet, basename="application")
router.register("feedback", FeedbackViewSet, basename="feedback")
router.register("FAQ", FAQViewSet, basename="FAQ")
router.register("mentors", MentorProfileViewSet, basename="mentorprofile")

urlpatterns = [
    path("", include(router.urls)),
]
