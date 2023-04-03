from django.urls import path

from rest_framework.routers import SimpleRouter

from .views import FormParlerViewSet

router = SimpleRouter()
router.register("forms", FormParlerViewSet, basename="form")

urlpatterns = router.urls
