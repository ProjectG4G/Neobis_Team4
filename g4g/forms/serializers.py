from rest_framework import serializers
from rest_framework.validators import ValidationError

from parler_rest.serializers import TranslatableModelSerializer, TranslatedFieldsField

from .models import (
    Event,
    EventImage,
    Form,
    Question,
    Choice,
    Application,
    Response,
)

from .utils import upload_images


class EventImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventImage
        fields = (
            "id",
            "url",
            "event",
            "image",
        )


class EventParlerSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=Event, required=False)

    images = EventImageSerializer(many=True, read_only=True)
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(),
        allow_empty=True,
        required=False,
        write_only=True,
    )

    class Meta:
        model = Event
        fields = (
            "id",
            "url",
            "type",
            "translations",
            "images",
            "uploaded_images",
            "created_at",
            "updated_at",
        )

    def create(self, validated_data):
        uploaded_images = validated_data.pop("uploaded_images", [])

        event = Event.objects.create(**validated_data)

        event.save()

        upload_images(images=uploaded_images, event=event)

        return event

    def update(self, instance, validated_data):
        uploaded_images = validated_data.pop("uploaded_image", [])

        upload_images(images=uploaded_images, event=instance)

        return super().update(instance, validated_data)


class QuestionChoiceSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Choice
        fields = (
            "id",
            "url",
            "choice_text",
        )


class QuestionSerializer(serializers.ModelSerializer):
    choices = QuestionChoiceSerializer(many=True, required=False)

    class Meta:
        model = Question
        fields = (
            "id",
            "url",
            "title",
            "description",
            "form",
            "question_type",
            "choices",
            "required",
        )
        # depth = 1

    def create(self, validated_data):
        choices_data = validated_data.pop("choices", [])

        question = Question.objects.create(**validated_data)

        for choice in choices_data:
            Choice.objects.create(question=question, **choice)

        return question

    def update(self, instance, validated_data):
        choices_data = validated_data.pop("choices")
        choices = instance.choices.all()
        choices = list(choices)

        instance.title = validated_data.get("title", instance.title)
        instance.description = validated_data.get("description", instance.description)
        instance.question_type = validated_data.get(
            "question_type", instance.question_type
        )
        instance.required = validated_data.get("required", instance.required)

        instance.save()

        for choice_data in choices_data:
            if "id" in choice_data:
                choice = choices.pop(
                    choices.index(Choice.objects.get(id=choice_data["id"]))
                )

                choice.choice_text = choice_data.get("choice_text", choice.choice_text)

                choice.save()

            else:
                Choice.objects.create(question=instance, **choice_data)

        for choice in choices:
            choice.delete()

        return instance


class FormParlerSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=Form)

    questions = QuestionSerializer(many=True, required=False)

    class Meta:
        model = Form
        fields = (
            "id",
            "url",
            "event",
            "translations",
            "created_at",
            "updated_at",
            "active",
            "questions",
        )


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = (
            "id",
            "url",
            "choice_text",
            "question",
        )


class ResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Response
        fields = (
            "id",
            "url",
            "question",
            "application",
            "response_text",
            "response_choices",
            "response_file",
        )

    def create(self, validated_data):
        choices_data = validated_data.pop("response_choices", [])

        response = Response.objects.create(**validated_data)

        for choice_data in choices_data:
            choice = Choice.objects.get(id=choice_data.id)
            response.response_choices.add(choice)
        return response

    def validate(self, attrs):
        question = attrs["question"]
        application = attrs["application"]

        if Response.objects.filter(question=question, application=application).exists():
            raise ValidationError(
                {"detail": "Response for question already exists in Application!"}
            )

        response_file = attrs.get("response_file", None)

        choices_data = attrs.get("response_choices", [])
        response_text = attrs.get("response_text", "")

        if question.question_type == "file":
            if not response_file and question.required:
                raise ValidationError({"detail": "File must be uploaded!"})
            if choices_data or response_text:
                raise ValidationError({"detail": "Only File must be uploaded!"})

        if question.question_type in ["text", "paragraph"]:
            if choices_data:
                raise ValidationError(
                    {"detail": "Text based Question cannot have choices as Response!"}
                )
            if response_text == "" and question.required:
                raise ValidationError({"detail": "Text based Response can't be empty!"})

        if question.question_type == "multiple_choice":
            if len(choices_data) != 1 and question.required:
                raise ValidationError(
                    {
                        "detail": "Multiple-choice Question should have one choice as Response!"
                    }
                )

        if question.question_type == "checkbox":
            if len(choices_data) == 0 and question.required:
                raise ValidationError(
                    {
                        "detail": "Checkbox type of Question must have at least one Choice as Response!"
                    }
                )

        for choice in choices_data:
            if choice.question != question:
                raise ValidationError(
                    {
                        "detail": f"This Choice - {choice} doesn't belong to Question - {question}"
                    }
                )

        return attrs


class ApplicationSerializer(serializers.ModelSerializer):
    last_name = serializers.CharField(source="user.last_name", read_only=True)
    first_name = serializers.CharField(source="user.first_name", read_only=True)
    email = serializers.CharField(source="user.email", read_only=True)
    phone_number = serializers.CharField(source="user.phone_number", read_only=True)
    region = serializers.CharField(source="user.region", read_only=True)
    district = serializers.CharField(source="user.district", read_only=True)
    village = serializers.CharField(source="user.village", read_only=True)

    responses = ResponseSerializer(many=True, read_only=True)

    class Meta:
        model = Application
        fields = (
            "id",
            "url",
            "form",
            "status",
            "user",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "region",
            "district",
            "village",
            "responses",
            "created_at",
            "updated_at",
        )


class ApplicationCreateSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(allow_blank=True, required=False)

    class Meta:
        model = Application
        fields = (
            "id",
            "url",
            "form",
            "phone_number",
            "user",
        )

        read_only_fields = ("user",)

    def create(self, validated_data):
        request = self.context.get("request")

        user = request.user if request and hasattr(request, "user") else None

        validated_data["user"] = user
        validated_data["status"] = "filling"
        phone_number = validated_data.pop("phone_number", None)
        if user.phone_number is None:
            user.phone_number = phone_number
            user.save()

        response = super().create(validated_data)

        return response


class ResponseMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Response
        fields = (
            "question",
            "application",
            "response_text",
            "response_choices",
            "response_file",
        )


class ApplicationExcelSerializer(serializers.ModelSerializer):
    last_name = serializers.CharField(source="user.last_name", read_only=True)
    first_name = serializers.CharField(source="user.first_name", read_only=True)
    email = serializers.CharField(source="user.email", read_only=True)
    phone_number = serializers.CharField(source="user.phone_number", read_only=True)

    responses = ResponseSerializer(many=True, read_only=True)

    extra_fields = serializers.SerializerMethodField()

    def get_extra_fields(self, obj):
        extra_fields = {}

        # loop through any additional fields you want to add
        for field_name in "some":
            extra_fields[field_name] = obj.user.last_name

        return extra_fields

    class Meta:
        model = Application
        fields = (
            "form",
            "status",
            "user",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "responses",
            "created_at",
            "updated_at",
            "extra_fields",
        )

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        responses = representation["responses"]

        representation.pop("responses")

        if responses:
            for response in responses:
                question = Question.objects.get(id=response["question"])

                if question.question_type in ["text", "paragraph"]:
                    representation[f"{question.title}"] = response["response_text"]
                if question.question_type in ["multiple_choice", "checkbox"]:
                    representation[f"{question.title}"] = response["response_choices"]
                if question.question_type == "file":
                    representation[f"{question.title}"] = response["response_file"]

        print(representation)

        return representation
