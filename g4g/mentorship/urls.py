from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import (
    MentorProfileViewSet,
)

router = SimpleRouter()

router.register("mentors", MentorProfileViewSet, basename="mentorprofile")

urlpatterns = [
    path("", include(router.urls)),
]
