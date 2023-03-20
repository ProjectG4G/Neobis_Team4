from rest_framework.serializers import ModelSerializer
from .models import FAQ, Rating, Comment, Trainings, TrainingsImage, TrainingsApplications, TrainingsQuestions
from rest_framework import serializers


class TrainingsImageSerializer(ModelSerializer):
    class Meta:
        model = TrainingsImage
        fields = "__all__"


class TrainingsSerializer(ModelSerializer):
    images = TrainingsImageSerializer(many=True, read_only=True)
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(allow_empty_file=False, use_url=False),
        write_only=True,
        required=False
    )

    class Meta:
        model = Trainings
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

        trainings = Trainings.objects.create(**validated_data)

        for image in uploaded_images:
            TrainingsImage.objects.create(trainigs=trainings, image=image)

        return trainings


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class RatingSerializer(ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'


class FAQSerializer(ModelSerializer):
    class Meta:
        model = FAQ
        fields = '__all__'


class ApplicationsSerializer(ModelSerializer):
    class Meta:
        model = TrainingsApplications
        fields = '__all__'


class QuestionsSerializer(ModelSerializer):
    class Meta:
        model = TrainingsQuestions
        fields = '__all__'
