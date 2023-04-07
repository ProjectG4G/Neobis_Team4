from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import viewsets, filters
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from .permissions import IsAdminOrReadOnly

from .serializers import TrainingsParlerSerializer
from .models import Trainings


class TrainingsParlerViewSet(viewsets.ModelViewSet):
    queryset = Trainings.objects.all()
    serializer_class = TrainingsParlerSerializer
    permission_classes = [AllowAny]
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filter_fields = ["title"]
    search_fields = (
        "title",
        "content",
        "header1",
        "header2",
    )
