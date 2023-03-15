from rest_framework.serializers import ModelSerializer
from .models import Mentorship, Applications, Feedback, FAQ


class MentorshipSerializer(ModelSerializer):
    class Meta:
        model = Mentorship
        fields = '__all__'


class ApplicationsSerializer(ModelSerializer):
    class Meta:
        model = Applications
        fields = '__all__'


class FeedbackSerializer(ModelSerializer):
    class Meta:
        model = Feedback
        fields = '__all__'


class FAQSerializer(ModelSerializer):
    class Meta:
        model = FAQ
        fields = '__all__'
