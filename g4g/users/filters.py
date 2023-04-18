from django_filters import FilterSet, fields
from .models import User


class UserFilter(FilterSet):
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "region",
            "district",
            "village",
            "region__name",
            "district__name",
            "village__name",
            "is_staff",
            "is_mentor",
            "is_superuser",
            "is_active",
            "is_verified",
        ]
