from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views import TrainingsViewSet, CommentViewSet, RatingViewSet, FAQViewSet, QuestionsViewSet, ApplicationsViewSet

router = SimpleRouter()
router.register('trainings', TrainingsViewSet, basename='training')
router.register('questions', QuestionsViewSet, basename='questions')
router.register('applications', ApplicationsViewSet, basename='applications')
router.register('comments', CommentViewSet, basename='comment')
router.register('ratings', RatingViewSet, basename='rating')
router.register('FAQ', FAQViewSet, basename='FAQ')


urlpatterns = [
    path('', include(router.urls)),
]
