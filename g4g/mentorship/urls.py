from django.urls import path, include, reverse

from rest_framework.routers import SimpleRouter
from rest_framework.views import APIView
from rest_framework.response import Response

from .views import (
    MentorProfileViewSet,
    MentorshipViewSet,
    MenteeViewSet,
    MentorshipApplicationsViewSet,
)

router = SimpleRouter()

router.register("mentors", MentorProfileViewSet, basename="mentorprofile")
router.register("mentees", MenteeViewSet, basename="mentee")
router.register("programs", MentorshipViewSet, basename="programs")
router.register(
    "applications", MentorshipApplicationsViewSet, basename="mentorshipapplication"
)


class ListUrlsView(APIView):
    def get(self, request, format=None):
        url_list = [
            request.build_absolute_uri(reverse("mentorprofile-list")),
            request.build_absolute_uri(reverse("mentee-list")),
            request.build_absolute_uri(reverse("programs-list")),
        ]
        return Response(url_list)


urlpatterns = [
    path("", include(router.urls)),
    path("", ListUrlsView.as_view(), name="urls"),
]
