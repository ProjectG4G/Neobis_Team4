from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet

from .serializers import MentorshipSerializer, ApplicationsSerializer, FAQSerializer, FeedbackSerializer, QuestionSerializer
from .models import Mentorship, FAQ, Feedback, Applications, Questions
from .permissions import IsAdminOrReadOnly


class MentorshipViewSet(ModelViewSet):
    queryset = Mentorship.objects.all()
    serializer_class = MentorshipSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['title']


class QuestionsViewSet(ModelViewSet):
    queryset = Questions.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAdminOrReadOnly]


class ApplicationsViewSet(ModelViewSet):
    queryset = Applications.objects.all()
    serializer_class = ApplicationsSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['district', 'name']
    permission_classes = [IsAdminOrReadOnly]


class FeedbackViewSet(ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = [IsAdminOrReadOnly]


class FAQViewSet(ModelViewSet):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer
    permission_classes = [IsAdminOrReadOnly]
