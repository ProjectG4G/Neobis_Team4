from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from drf_spectacular.utils import extend_schema

from forms.models import Event, Application
from forms.serializers import EventParlerSerializer, ApplicationSerializer
from forms.views import ApplicationViewSet

from .serializers import (
    MentorProfileSerializer,
    MenteeSerializer,
)
from .models import (
    MentorProfile,
    Mentee,
)

from .permissions import IsAdminOrReadOnly


@extend_schema(tags=["Mentorship Programs"])
class MentorshipViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.filter(type="mentorship")
    serializer_class = EventParlerSerializer

    permission_classes = (IsAdminOrReadOnly,)


@extend_schema(tags=["Mentees"])
class MenteeViewSet(viewsets.ModelViewSet):
    queryset = Mentee.objects.all()
    serializer_class = MenteeSerializer

    permission_classes = (IsAdminOrReadOnly,)


@extend_schema(tags=["Mentor Profiles"])
class MentorProfileViewSet(viewsets.ModelViewSet):
    queryset = MentorProfile.objects.all()
    serializer_class = MentorProfileSerializer

    permission_classes = [IsAdminOrReadOnly]


@extend_schema(tags=["Mentorship Applications"])
class MentorshipApplicationsViewSet(ApplicationViewSet):
    queryset = Application.objects.filter(form__event__type="mentorship")
