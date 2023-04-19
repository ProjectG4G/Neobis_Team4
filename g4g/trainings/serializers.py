from rest_framework import serializers

from .models import Applicant


class TrainingApplicantSerializer(serializers.ModelSerializer):
    last_name = serializers.CharField(source="user.last_name", read_only=True)
    first_name = serializers.CharField(source="user.first_name", read_only=True)

    class Meta:
        model = Applicant
        fields = (
            "id",
            "last_name",
            "first_name",
            "training",
        )
