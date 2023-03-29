from django.urls import path, include

from rest_framework.routers import SimpleRouter

from .views import TagViewSet, ArticleViewSet, ArticleImageViewSet

router = SimpleRouter()
router.register('tags', TagViewSet, basename='article-tag')
router.register('articles', ArticleViewSet, basename='article')
router.register('images', ArticleImageViewSet, basename='article-image')

urlpatterns = [
    path('', include(router.urls)),
]
