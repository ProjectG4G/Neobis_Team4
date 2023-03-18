from rest_framework.serializers import ModelSerializer
from .models import Mentorship, Applications, Feedback, FAQ, Questions, MentorshipImage
from rest_framework import serializers


class MentorshipImageSerializer(ModelSerializer):
    class Meta:
        model = MentorshipImage
        fields = "__all__"


class MentorshipSerializer(ModelSerializer):
    images = MentorshipImageSerializer(many=True, read_only=True)

    uploaded_images = serializers.ListField(
        child=serializers.ImageField(allow_empty_file=False, use_url=False),
        write_only=True,
        required=False
    )

    class Meta:
        model = Mentorship
        fields = [
            'id',
            'date',
            'title',
            'content',
            'images',
            'link',
            'uploaded_images',
        ]

    def create(self, validated_data):
        uploaded_images = validated_data.pop("uploaded_images")

        mentorship = Mentorship.objects.create(**validated_data)

        for image in uploaded_images:
            MentorshipImage.objects.create(mentorship=mentorship, image=image)

        return mentorship


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


class QuestionSerializer(ModelSerializer):
    class Meta:
        model = Questions
        fields = '__all__'
