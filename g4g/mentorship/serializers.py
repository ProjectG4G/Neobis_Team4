from rest_framework import serializers

from .models import (
    MentorProfile,
    Mentee,
)


class MenteeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mentee
        fields = (
            "id",
            "url",
            "program",
            "user",
        )


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
            "programs",
            "mentees",
        )

        read_only_fields = ("user",)
