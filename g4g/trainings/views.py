from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.viewsets import ModelViewSet
from .permissions import IsAdminOrReadOnly

from .serializers import (
    TrainingsSerializer,
    CommentSerializer,
    RatingSerializer,
    FAQSerializer,
    ApplicationsSerializer,
    QuestionsSerializer,
)
from .models import Trainings, Comment, Rating, FAQ, TrainingsQuestions, TrainingsApplications


class TrainingsViewSet(ModelViewSet):
    queryset = Trainings.objects.all()
    serializer_class = TrainingsSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['title']


class QuestionsViewSet(ModelViewSet):
    queryset = TrainingsQuestions.objects.all()
    serializer_class = QuestionsSerializer
    permission_classes = [IsAdminOrReadOnly]


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAdminOrReadOnly]


class FAQViewSet(viewsets.ModelViewSet):
    serializer_class = FAQSerializer
    queryset = FAQ.objects.all()
    permission_classes = [IsAdminOrReadOnly]


class RatingViewSet(viewsets.ModelViewSet):
    serializer_class = RatingSerializer
    queryset = Rating.objects.all()
    permission_classes = [IsAdminOrReadOnly]


class ApplicationsViewSet(ModelViewSet):
    queryset = TrainingsApplications.objects.all()
    serializer_class = ApplicationsSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['district', 'name']
    permission_classes = [IsAdminOrReadOnly]
