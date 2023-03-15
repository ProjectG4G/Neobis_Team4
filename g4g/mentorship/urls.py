from django.urls import path, include
from rest_framework.routers import SimpleRouter

from mentorship.views import MentorshipViewSet, ApplicationsViewSet, FeedbackViewSet, FAQViewSet

router = SimpleRouter()
router.register('mentorship', MentorshipViewSet, basename='mentorship')
router.register('applications', ApplicationsViewSet, basename='applications')
router.register('feedback', FeedbackViewSet, basename='feedback')
router.register('FAQ', FAQViewSet, basename='FAQ')


urlpatterns = [
    path('', include(router.urls)),
]
