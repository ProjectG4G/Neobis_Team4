from rest_framework import viewsets
from .models import VideoCategory, Video, Comment
from .serializers import VideoCategorySerializer, VideoSerializer, CommentSerializer


class RecentVideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.order_by("-created_at")[:5]
    serializer = VideoSerializer


class VideoCategoryViewSet(viewsets.ModelViewSet):
    queryset = VideoCategory.object.all
    serializer = VideoCategorySerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.object.all
    serializer = CommentSerializer
