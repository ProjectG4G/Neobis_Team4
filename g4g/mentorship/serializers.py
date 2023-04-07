from rest_framework import serializers
from parler_rest.serializers import TranslatableModelSerializer, TranslatedFieldsField

from forms.models import Form
from .models import (
    Mentorship,
    MentorshipImage,
    MentorProfile,
)

from forms.utils import get_language, switch_language


class MentorshipImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = MentorshipImage
        fields = "__all__"


class MentorshipParlerSerializer(TranslatableModelSerializer):
    images = MentorshipImageSerializer(many=True, read_only=True)
    translations = TranslatedFieldsField(shared_model=Mentorship)

    class Meta:
        model = Mentorship
        fields = "__all__"
        extra_fields = "translations"


class MentorshipCreateUpdateSerializer(serializers.ModelSerializer):
    title = serializers.CharField(required=True, allow_blank=True, write_only=True)
    descriptions = serializers.CharField(required=True, allow_blank=True, write_only=True)

    class Meta:
        model = Form
        fields = "__all__"
        extra_fields = "translations"

    def create(self, validated_data):
        title = validated_data.pop("title", "")
        description = validated_data.pop("description", "")
        form = Form.objects.create(**validated_data)
        lang = get_language(self)
        form.set_current_language(lang)
        form.title = title
        form.description = description
        form.set_current_language(switch_language(lang))
        form.title = ""
        form.description = ""
        form.set_current_language()

    def update(self, form, validated_data):
        title = validated_data.pop("title", "")
        description = validated_data.pop("description", "")
        form.set_current_language(get_language(self))
        form.title = title
        form.description = description
        form.save()
        return form


class MentorProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source="user.first_name", read_only=True)
    last_name = serializers.CharField(source="user.last_name", read_only=True)

    profile_picture = serializers.ImageField(
        source="user.profile_picture", read_only=True
    )

    class Meta:
        model = MentorProfile
        fields = (
            "id",
            "user",
            "url",
            "first_name",
            "last_name",
            "profile_picture",
            "image",
            "description",
        )
        read_only_fields = ("user",)
