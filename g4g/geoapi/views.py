import json

from django.conf import settings

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import (
    CountrySerializer,
    CitySerializer,
    RegionSerializer,
    DistrictSerializer,
    VillageSerializer,
)

from .models import (
    Country,
    City,
    Region,
    District,
    Village,
)


class CountryViewSet(ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


class RegionViewSet(ModelViewSet):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


class CityViewSet(ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


class DistrictViewSet(ModelViewSet):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


class VillageViewSet(ModelViewSet):
    queryset = Village.objects.all()
    serializer_class = VillageSerializer

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


class GeoDataAPIView(APIView):
    def get(self, request, *args, **kwargs):
        with open(settings.STATIC_ROOT + 'geodata/geodata.json', 'r') as file:
            data = json.load(file)
        return Response(data)
