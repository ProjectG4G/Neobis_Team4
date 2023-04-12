from django.urls import path, include

from rest_framework.routers import SimpleRouter

from .views import TrainingViewSet

router = SimpleRouter()
router.register("trainings", TrainingViewSet, basename="training")

urlpatterns = [
    path("", include(router.urls)),
]
