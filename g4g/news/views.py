from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import ArticleSerializer, TagSerializer, ArticleAddTagsSerializer
from .models import Article, Tag
from .permissions import IsAdminOrReadOnly


# Create your views here.

class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class ArticleViewSet(ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'add_tags':
            return ArticleAddTagsSerializer
        return ArticleSerializer

    @action(detail=True, methods=['put'])
    def add_tags(self, request, pk=None):
        serializer = ArticleAddTagsSerializer(data=request.data)

        if serializer.is_valid():
            article = Article.objects.get(pk=pk)
            serializer.update(instance=article, validated_data=serializer.validated_data)
            return Response({
                'detail': 'tags were added',
                'data': serializer.data,
            })
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
