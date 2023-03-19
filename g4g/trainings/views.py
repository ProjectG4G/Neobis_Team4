from django_filters.rest_framework import DjangoFilterBackend
from mentorship.serializers import QuestionSerializer
from rest_framework import viewsets
from rest_framework.viewsets import ModelViewSet
from .permissions import IsAdminOrReadOnly

from .serializers import TrainingsSerializer, CommentSerializer, RatingSerializer, FAQSerializer
from .models import Trainings, Comment, Rating, FAQ, Questions


class TrainingsViewSet(ModelViewSet):
    queryset = Trainings.objects.all()
    serializer_class = TrainingsSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['title']


class QuestionsViewSet(ModelViewSet):
    queryset = Questions.objects.all()
    serializer_class = QuestionSerializer
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
