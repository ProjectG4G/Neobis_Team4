from django.urls import path, include
from rest_framework.routers import SimpleRouter

from mentorship.views import MentorshipViewSet, ApplicationsViewSet, FeedbackViewSet, FAQViewSet, QuestionsViewSet

router = SimpleRouter()
router.register('mentorships', MentorshipViewSet, basename='mentorship')
router.register('questions', QuestionsViewSet , basename='questions')
router.register('applications', ApplicationsViewSet, basename='applications')
router.register('feedback', FeedbackViewSet, basename='feedback')
router.register('FAQ', FAQViewSet, basename='FAQ')


urlpatterns = [
    path('', include(router.urls)),
]
