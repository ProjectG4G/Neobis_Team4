from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import viewsets, filters
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from .permissions import IsAdminOrReadOnly

from .serializers import (
    TrainingsSerializer,
    TrainingCommentSerializer,
    TrainingRatingSerializer,
    TrainingFAQSerializer,
    TrainingApplicationsSerializer,
    TrainingQuestionsSerializer,
)

from .models import (
    Trainings,
    Comment,
    Rating,
    FAQ,
    TrainingsQuestions,
    TrainingsApplications,
)


class TrainingsViewSet(ModelViewSet):
    queryset = Trainings.objects.all()
    serializer_class = TrainingsSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filter_fields = ['title']
    search_fields = ('title', 'content', 'header1', 'header2',)


class QuestionsViewSet(ModelViewSet):
    queryset = TrainingsQuestions.objects.all()
    serializer_class = TrainingQuestionsSerializer
    permission_classes = [IsAdminOrReadOnly]


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = TrainingCommentSerializer
    permission_classes = [IsAdminOrReadOnly]


class FAQViewSet(viewsets.ModelViewSet):
    serializer_class = TrainingFAQSerializer
    queryset = FAQ.objects.all()
    permission_classes = [IsAdminOrReadOnly]


class RatingViewSet(viewsets.ModelViewSet):
    serializer_class = TrainingRatingSerializer
    queryset = Rating.objects.all()
    permission_classes = [IsAdminOrReadOnly]


class ApplicationsViewSet(ModelViewSet):
    queryset = TrainingsApplications.objects.all()
    serializer_class = TrainingApplicationsSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['district', 'name']
    permission_classes = [IsAdminOrReadOnly]

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminOrReadOnly]

        return [permission() for permission in permission_classes]
