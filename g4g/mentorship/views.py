from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

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

    permission_classes = [IsAdminOrReadOnly]

    @action(methods=["put"], detail=True)
    def accept(self, request, pk=None):
        application = self.get_object()

        program = application.form.event

        mentee = Mentee.objects.create(
            program=application.form.event, user=application.user
        )

        mentor = (
            MentorProfile.objects.annotate(num_mentees=Count("mentees"))
            .filter(programs=program)
            .order_by("num_mentees")
        )[0]

        mentor.mentees.add(mentee)

        mentor.save()

        application.status = "accepted"

        application.save()

        return Response(
            {
                "detail": "Application accepted, Mentor {} was assigned to mentee {}!".format(
                    mentor, mentee
                )
            }
        )
