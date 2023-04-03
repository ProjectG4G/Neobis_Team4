from rest_framework import serializers
from parler_rest.serializers import TranslatableModelSerializer, TranslatedFieldsField

from .models import Form, Question, FormBase


class FormParlerSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=Form)

    class Meta:
        model = Form
        fields = (
            "id",
            "url",
            "translations",
            "created",
            "edited",
            "formbase",
            "active",
        )
