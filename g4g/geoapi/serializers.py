from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework.serializers import ListField, DictField

from .models import (
    Country,
    Region,
    City,
    District,
    Village,
)


class CountrySerializer(ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'


class RegionSerializer(ModelSerializer):
    class Meta:
        model = Region
        fields = '__all__'


class CitySerializer(ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'


class DistrictSerializer(ModelSerializer):
    class Meta:
        model = District
        fields = '__all__'


class VillageSerializer(ModelSerializer):
    class Meta:
        model = Village
        fields = '__all__'


class GeoAPIJSONDataSerializer(Serializer):
    regions = ListField()
    districts = DictField(child=ListField())
    villages = DictField(child=ListField())
