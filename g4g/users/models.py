from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number=None, email=None, password=None, **extra_fields):
        if not phone_number and not email:
            raise ValueError(_("Phone number or email must be specified for users."))
        elif phone_number and not email:
            user = self.model(
                username=phone_number,
                **extra_fields,
            )
        elif not phone_number and email:
            user = self.model(
                email=email,
                **extra_fields,
            )
        else:
            user = self.model(
                email=email,
                phone_number=phone_number,
                **extra_fields,
            )

        user.set_password(password)
        user.save()

        return user

    def create_superuser(
            self, phone_number=None, email=None, password=None, **extra_fields
    ):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_stuff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        if extra_fields.get("is_active") is not True:
            raise ValueError(_("Superuser must have is_active=True."))

        return self.create_user(
            phone_number=phone_number,
            password=password,
            email=email,
            **extra_fields,
        )


class User(AbstractUser):
    username = None

    phone_number = models.CharField(
        max_length=12,
        null=True,
        unique=True,
        blank=True,
    )

    email = models.EmailField(
        _("Email address"),
        max_length=255,
        null=True,
        unique=True,
    )

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ()

    objects = CustomUserManager()

    country = models.CharField(max_length=50)
    # TODO add choice fields ?
    region = models.CharField(max_length=50)
    district = models.CharField(max_length=50)

    def __str__(self) -> str:
        return "{}".format(self.username)