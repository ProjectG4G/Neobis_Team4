from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import viewsets, filters

from rest_framework.decorators import action

from drf_spectacular.utils import extend_schema

from django_filters.rest_framework import DjangoFilterBackend

from forms.models import Event
from forms.views import (
    ApplicationViewSet,
    EventParlerViewSet,
    FormParlerViewSet,
)

from forms.models import Application, Form

from .utils import accept_training

from .permissions import IsAdminOrReadOnly

from .models import Applicant

from .serializers import TrainingApplicantSerializer


@extend_schema(tags=["Trainings"])
class TrainingViewSet(EventParlerViewSet):
    queryset = Event.objects.filter(type="training")


@extend_schema(tags=["Training Applications"])
class TrainingApplicationViewSet(ApplicationViewSet):
    queryset = Application.objects.filter(form__event__type="training")

    @action(methods=["put"], detail=True)
    def accept(self, request, pk=None):
        return accept_training(self, self.get_object())


@extend_schema(tags=["Training Forms"])
class TrainingsFormViewSet(FormParlerViewSet):
    queryset = Form.objects.filter(event__type="training")


@extend_schema(tags=["Training Accepted Applicant"])
class TrainingApplicantViewSet(viewsets.ModelViewSet):
    queryset = Applicant.objects.all()
    serializer_class = TrainingApplicantSerializer

    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
    )

    filterset_fields = ("training",)
