from django.urls import path, include

from rest_framework.routers import SimpleRouter

from .views import (
    TagViewSet,
    ArticleImageViewSet,
    ArticleParlerViewSet,
)

router = SimpleRouter()
router.register("tags", TagViewSet, basename="tag")
router.register("images", ArticleImageViewSet, basename="articleimage")
router.register("articles", ArticleParlerViewSet, basename="article")

urlpatterns = [
    path("", include(router.urls)),
]
