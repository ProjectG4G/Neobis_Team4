from rest_framework import serializers

from geoapi.models import (
    Region,
    District,
    Village,
)

from .models import (
    Mentorship,
    MentorshipApplications,
    Feedback,
    FAQ,
    MentorshipQuestions,
    MentorshipImage,
    MentorProfile,
)


class MentorshipImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = MentorshipImage
        fields = "__all__"


class MentorshipSerializer(serializers.ModelSerializer):
    images = MentorshipImageSerializer(many=True, read_only=True)

    uploaded_images = serializers.ListField(
        child=serializers.ImageField(
            allow_empty_file=True, use_url=False, required=False
        ),
        write_only=True,
        required=False,
    )

    class Meta:
        model = Mentorship
        fields = [
            "id",
            "created",
            "edited",
            "title",
            "header1",
            "header2",
            "body1",
            "body2",
            "body3",
            "images",
            "uploaded_images",
        ]

    def create(self, validated_data):
        uploaded_images = None
        if validated_data.__contains__("uploaded_images"):
            uploaded_images = validated_data.pop("uploaded_images")

        mentorship = Mentorship.objects.create(**validated_data)

        for image in uploaded_images:
            MentorshipImage.objects.create(mentorship=mentorship, image=image)

        return mentorship


class ApplicationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MentorshipApplications
        fields = "__all__"
        read_only_fields = ("user", "is_accepted")

    def validate(self, attrs):
        region = attrs["region"]
        district = attrs["district"]
        village = attrs["village"]

        if not Region.objects.filter(id=region.id).exists():
            raise serializers.ValidationError(
                {"detail": "Given region {} does not exist!".format(region)}
            )

        if not District.objects.filter(id=district.id).exists():
            raise serializers.ValidationError(
                {"detail": "Given district/city {} does not exist!".format(district)}
            )

        if village and not Village.objects.filter(id=village.id).exists():
            raise serializers.ValidationError(
                {"detail": "Given village {} does not exist!".format(village)}
            )

        if district.region != region:
            raise serializers.ValidationError(
                {
                    "detail": "Given district or city {} doesn't belong to region {}".format(
                        district, region
                    )
                }
            )

        if village and village.district != district:
            raise serializers.ValidationError(
                {
                    "detail": "Given village {} doesn't belong to district {}".format(
                        village, district
                    )
                }
            )

        return attrs

    def create(self, validated_data):
        request = self.context.get("request")

        validated_data["user"] = request.user

        application = MentorshipApplications.objects.create(**validated_data)

        return application


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = "__all__"


class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = "__all__"


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MentorshipQuestions
        fields = "__all__"


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
