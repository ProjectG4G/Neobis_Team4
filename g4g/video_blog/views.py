from rest_framework import viewsets
from .models import Playlist, Video, Comment, RecentlyWatched
from .serializers import PlaylistSerializer, VideoSerializer, CommentSerializer, RecentlyWatchedSerializer


class VideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer


class RecentlyWatchedViewSet(viewsets.ModelViewSet):
    serializer_class = RecentlyWatchedSerializer

    def get_queryset(self):
        user = self.request.user
        return RecentlyWatched.objects.filter(user=user).order_by('-timestamp')[:10]


class PlaylistViewSet(viewsets.ModelViewSet):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
