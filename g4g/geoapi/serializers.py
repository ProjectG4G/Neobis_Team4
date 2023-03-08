from rest_framework.serializers import ModelSerializer

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
