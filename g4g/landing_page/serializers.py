from rest_framework.serializers import ModelSerializer
from .models import LandingPage


class LandingPageSerializer(ModelSerializer):
    class Meta:
        model = LandingPage
        fields = '__all__'
