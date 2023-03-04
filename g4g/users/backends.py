from django.contrib.auth.backends import BaseBackend
from django.db.models import Q

from django.contrib.auth import get_user_model

User = get_user_model()


class EmailOrPhoneBackend(BaseBackend):
    def authenticate(self, request, email=None, phone_number=None, password=None, **kwargs):

        try:
            # Try to fetch the user by searching the username or email field
            if email is not None:
                user = User.objects.get(Q(email=email))
            else:
                user = User.objects.get(Q(phone_number=phone_number))
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a non-existing user (#20760).
            User().set_password(password)
