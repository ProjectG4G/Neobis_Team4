from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import viewsets, filters

from drf_spectacular.utils import extend_schema

from forms.models import Event
from forms.serializers import EventParlerSerializer

from .permissions import IsAdminOrReadOnly


@extend_schema(tags=["Trainings"])
class TrainingViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.filter(type="training")
    serializer_class = EventParlerSerializer

    permission_classes = (IsAdminOrReadOnly,)

    filter_fields = (
        "title",
        "",
    )
