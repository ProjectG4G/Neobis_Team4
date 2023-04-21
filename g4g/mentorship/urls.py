from django.urls import path, include, reverse

from rest_framework.routers import SimpleRouter
from rest_framework.views import APIView
from rest_framework.response import Response

from .views import (
    MentorProfileViewSet,
    MentorshipViewSet,
    MenteeViewSet,
    MentorshipApplicationsViewSet,
    MentorshipFormViewSet,
)

router = SimpleRouter()

router.register("mentors", MentorProfileViewSet, basename="mentorprofile")
router.register("mentees", MenteeViewSet, basename="mentee")
router.register("programs", MentorshipViewSet, basename="programs")
router.register("applications", MentorshipApplicationsViewSet, basename="application")
router.register("forms", MentorshipFormViewSet, basename="form")


urlpatterns = [
    path("", include(router.urls)),
]
