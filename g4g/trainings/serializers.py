from rest_framework.serializers import (
    ModelSerializer,
    ListField,
    ImageField,
)
from .models import (
    Trainings,
    TrainingsImage,
)
from parler_rest.serializers import TranslatableModelSerializer, TranslatedFieldsField


class TrainingsImageSerializer(ModelSerializer):
    class Meta:
        model = TrainingsImage
        fields = "__all__"


class TrainingsSerializer(ModelSerializer):
    images = TrainingsImageSerializer(many=True, read_only=True)
    uploaded_images = ListField(
        child=ImageField(allow_empty_file=False, use_url=False),
        write_only=True,
        required=False,
    )

    class Meta:
        model = Trainings
        fields = [
            "id",
            "title",
            "images",
            "uploaded_images",
        ]

    def create(self, validated_data):
        uploaded_images = validated_data.pop("uploaded_images")

        training = Trainings.objects.create(**validated_data)

        for image in uploaded_images:
            TrainingsImage.objects.create(training=training, image=image)

        return training


class TrainingsParlerSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=Trainings)

    class Meta:
        model = Trainings
        fields = "__all__"
        extra_fields = [
            "translations",
        ]
