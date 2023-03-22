from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from .serializers import (
    MentorshipSerializer,
    ApplicationsSerializer,
    FAQSerializer,
    FeedbackSerializer,
    QuestionSerializer,
    MentorProfileSerializer,
)
from .models import (
    Mentorship,
    FAQ,
    Feedback,
    MentorshipApplications,
    MentorshipQuestions,
    MentorProfile,
)

from .permissions import IsAdminOrReadOnly


class MentorshipViewSet(ModelViewSet):
    queryset = Mentorship.objects.all()
    serializer_class = MentorshipSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['title']


class QuestionsViewSet(ModelViewSet):
    queryset = MentorshipQuestions.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAdminOrReadOnly]


class ApplicationsViewSet(ModelViewSet):
    queryset = MentorshipApplications.objects.all()
    serializer_class = ApplicationsSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['title']

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminOrReadOnly]

        return [permission() for permission in permission_classes]


class FeedbackViewSet(ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = [IsAdminOrReadOnly]


class FAQViewSet(ModelViewSet):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer
    permission_classes = [IsAdminOrReadOnly]


class MentorProfileViewSet(ModelViewSet):
    queryset = MentorProfile.objects.all()
    serializer_class = MentorProfileSerializer
    permission_classes = [IsAdminOrReadOnly]

    allowed_methods = ['GET', 'PUT', 'PATCH', 'HEAD', 'OPTIONS']