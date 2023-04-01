from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Article, Tag, ArticleImage
from .permissions import IsAdminOrReadOnly
from .serializers import (
    TagSerializer,
    ArticleImageSerializer,
    ArticleReadOnlySerializer,
    ArticleCreateSerializer,
    ArticlePreCreateSerializer,
    ArticleUpdateSerializer,
    ArticleParlerSerializer,
)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAdminOrReadOnly,)


class ArticleImageViewSet(viewsets.ModelViewSet):
    queryset = ArticleImage.objects.all()
    serializer_class = ArticleImageSerializer
    permission_classes = (IsAdminOrReadOnly,)


class ArticleViewSet(viewsets.ModelViewSet):
    # permission_classes =

    def get_serializer_class(self):
        if self.action == "create":
            return ArticleCreateSerializer
        if self.action == "pre_create":
            return ArticlePreCreateSerializer
        if self.action in ["update", "partial_update"]:
            return ArticleUpdateSerializer
        return ArticleReadOnlySerializer

    def get_queryset(self):
        language = "ky"

        if "Accept-Language" in self.request.headers:
            language = self.request.headers["Accept-Language"]
            if language != "ru":
                language = "ky"

        return Article.objects.language(language).all()

    @action(detail=False, methods=["POST"])
    def pre_create(self, request):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(
                serializer.data,
                status.HTTP_201_CREATED,
            )

        return Response({"detail": "unable to create!"}, status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["GET"])
    def parler(self, request):
        queryset = Article.objects.all()
        serializer = ArticleParlerSerializer(queryset, many=True)

        return Response(serializer.data)
