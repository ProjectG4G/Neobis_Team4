from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.viewsets import ModelViewSet

from drf_spectacular.utils import extend_schema

from .serializers import (
    MentorProfileSerializer,
)
from .models import (
    MentorProfile,
)

from .permissions import IsAdminOrReadOnly


@extend_schema(tags=["Mentor Profiles"])
class MentorProfileViewSet(ModelViewSet):
    queryset = MentorProfile.objects.all()
    serializer_class = MentorProfileSerializer
    permission_classes = [IsAdminOrReadOnly]

    allowed_methods = ["GET", "PUT", "PATCH", "HEAD", "OPTIONS"]
