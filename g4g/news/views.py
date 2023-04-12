from rest_framework import viewsets
from drf_spectacular.utils import extend_schema

from .models import Article, Tag, ArticleImage
from .permissions import IsAdminOrReadOnly
from .serializers import (
    TagSerializer,
    ArticleImageSerializer,
    ArticleParlerSerializer,
)


@extend_schema(tags=["Article Tags"])
class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAdminOrReadOnly,)


@extend_schema(tags=["Article Images"])
class ArticleImageViewSet(viewsets.ModelViewSet):
    queryset = ArticleImage.objects.all()
    serializer_class = ArticleImageSerializer
    permission_classes = (IsAdminOrReadOnly,)


@extend_schema(tags=["Articles"])
class ArticleParlerViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()

    serializer_class = ArticleParlerSerializer
