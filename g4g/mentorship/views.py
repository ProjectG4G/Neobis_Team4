from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from .serializers import (
    MentorProfileSerializer,
)
from .models import (
    MentorProfile,
)

from .permissions import IsAdminOrReadOnly


class MentorProfileViewSet(ModelViewSet):
    queryset = MentorProfile.objects.all()
    serializer_class = MentorProfileSerializer
    permission_classes = [IsAdminOrReadOnly]

    allowed_methods = ["GET", "PUT", "PATCH", "HEAD", "OPTIONS"]
