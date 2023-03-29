from rest_framework import status, viewsets
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import (
    ArticleSerializer,
    TagSerializer,
    ArticleAddTagsSerializer,
    ArticleImageSerializer,
)
from .models import Article, Tag, ArticleImage
from .permissions import IsAdminOrReadOnly


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAdminOrReadOnly,)


class ArticleImageViewSet(viewsets.ModelViewSet):
    queryset = ArticleImage.objects.all()
    serializer_class = ArticleImageSerializer
    permission_classes = (IsAdminOrReadOnly,)


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsAdminOrReadOnly]
