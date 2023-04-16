from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import PlaylistViewSet, VideoViewSet, CommentViewSet, RecentlyWatchedViewSet


router = SimpleRouter()
router.register("playlists", PlaylistViewSet, basename="playlist")
router.register("videos", VideoViewSet, basename="video")
router.register("comments", CommentViewSet, basename="comment")
router.register("history", RecentlyWatchedViewSet, basename="recentlywatched")

urlpatterns = [
    path("", include(router.urls)),
]
