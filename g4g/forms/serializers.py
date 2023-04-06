from rest_framework import serializers
from parler_rest.serializers import TranslatableModelSerializer, TranslatedFieldsField

from .models import Form, Question, FormBase

from .utils import get_language, switch_language


class FormParlerSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=Form)

    class Meta:
        model = Form
        fields = (
            "id",
            "url",
            "translations",
            "created_at",
            "updated_at",
            "active",
        )


class FormReadOnlySerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField(read_only=True)
    description = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Form
        fields = (
            "title",
            "description",
            "active",
            "formbase",
            "created_at",
            "updated_at",
        )

    def get_title(self, obj):
        obj.set_current_language(get_language(self))
        return obj.title

    def get_description(self, obj):
        obj.set_current_language(get_language(self))
        return obj.descriptions


class FormCreateUpdateSerializer(serializers.ModelSerializer):
    title = serializers.CharField(required=True, allow_blank=True, write_only=True)
    description = serializers.CharField(required=True, allow_blank=True, write_only=True)

    class Meta:
        model = Form
        fields = (
            "id",
            "title",
            "description",
            "formbase",
        )

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

        form.set_current_language(lang)

        form.save()

        return form

    def update(self, form, validated_data):
        title = validated_data.pop("title", "")
        description = validated_data.pop("description", "")

        form.set_current_language(get_language(self))

        form.title = title
        form.description = description

        form.save()

        return form
