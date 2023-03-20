from django_filters import FilterSet
from .models import User


class UserFilter(FilterSet):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'region',
            'district',
            'village',
            'region__name',
            'district__name',
            'village__name',
            'is_staff',
            'is_mentor',
            # 'date_joined_day',
            # 'date_joined_month',
            # 'date_joined_year',
        ]
