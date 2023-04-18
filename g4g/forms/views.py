from rest_framework import viewsets
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
)

from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer

from drf_spectacular.utils import extend_schema

from drf_excel.mixins import XLSXFileMixin
from drf_excel.renderers import XLSXRenderer

from datetime import datetime

from .models import (
    Form,
    Event,
    Question,
    Choice,
    Response,
    Application,
    EventImage,
)

from .serializers import (
    EventParlerSerializer,
    FormParlerSerializer,
    QuestionSerializer,
    ApplicationSerializer,
    ApplicationCreateSerializer,
    ApplicationExcelSerializer,
    ResponseSerializer,
    EventImageSerializer,
    ChoiceSerializer,
)

from .permissions import IsAdminOrReadOnly


@extend_schema(
    tags=["Events"],
    description="Events include Trainings, Mentorship program.",
)
class EventParlerViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventParlerSerializer
    permission_classes = (IsAdminOrReadOnly,)


@extend_schema(
    tags=["Event Images"],
    description="Images for Events",
)
class EventImageViewSet(viewsets.ModelViewSet):
    queryset = EventImage.objects.all()
    serializer_class = EventImageSerializer
    permission_classes = (IsAdminOrReadOnly,)


@extend_schema(tags=["Forms"])
class FormParlerViewSet(viewsets.ModelViewSet):
    queryset = Form.objects.all()
    serializer_class = FormParlerSerializer
    permission_classes = (IsAdminOrReadOnly,)


@extend_schema(tags=["Form Questions"], description="Questions in Forms")
class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = (IsAdminOrReadOnly,)


@extend_schema(tags=["Questions Choices"], description="Choices in Question")
class ChoiceViewSet(viewsets.ModelViewSet):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer
    permission_classes = (IsAdminOrReadOnly,)


@extend_schema(tags=["Applications"], description="Application from users")
class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.action in ["retrieve", "list"]:
            return ApplicationSerializer
        else:
            return ApplicationCreateSerializer


@extend_schema(tags=["Applications Responses"])
class ResponseViewSet(viewsets.ModelViewSet):
    queryset = Response.objects.all()
    serializer_class = ResponseSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


@extend_schema(tags=["Applications Excel"])
class ApplicationExcelViewSet(XLSXFileMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Application.objects.all()

    serializer_class = ApplicationExcelSerializer

    renderer_classes = (
        BrowsableAPIRenderer,
        JSONRenderer,
        XLSXRenderer,
    )

    def get_filename(self, request=None, *args, **kwargs):
        return f"Mentorship Applications {datetime.now()}.xlsx"
