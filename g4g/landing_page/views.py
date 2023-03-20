from .models import LandingPage
from .serializers import LandingPageSerializer
from rest_framework import viewsets


class LandingPageViewSet(viewsets.ModelViewSet):
    serializer_class = LandingPageSerializer
    queryset = LandingPage.objects.all()

