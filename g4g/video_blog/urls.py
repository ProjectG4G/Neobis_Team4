from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .models import VideoCategory, Video, Comment
from .views import RecentVideoViewSet


router = SimpleRouter
router.register("category", VideoCategory, basename="category")
router.register("video", Video, basename="video")
router.register("comment", Comment, basename="comment")
router.register("recent_video", RecentVideoViewSet.as_view(), basename="recent_Video")

urlpatterns = [
    path("", include(router.urls)),
]
