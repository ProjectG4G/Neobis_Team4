from django.urls import path, include

from rest_framework.routers import SimpleRouter

from .views import TagViewSet, ArticleViewSet

router = SimpleRouter()
router.register('tags', TagViewSet, basename='tag')
router.register('articles', ArticleViewSet, basename='article')

urlpatterns = [
    path('', include(router.urls)),
]
