from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _

from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.urls import reverse
from django.conf import settings

from django_rest_passwordreset.signals import reset_password_token_created

from geoapi.models import Region, District, Village


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    """
    Handles password reset tokens
    When a token is created, an e-mail needs to be sent to the user
    :param sender: View Class that sent the signal
    :param instance: View Instance that sent the signal
    :param reset_password_token: Token Model Object
    :param args:
    :param kwargs:
    :return:
    """
    # send an e-mail to the user
    context = {
        'site_name': 'Girls for Girls',
        'current_user': reset_password_token.user,
        'username': reset_password_token.user.username,
        'email': reset_password_token.user.email,
        'reset_password_url': "{}?token={}".format(
            instance.request.build_absolute_uri(reverse('password_reset:reset-password-confirm')),
            reset_password_token.key),

        # TODO insert real contacts
        'company_address': _('Bishkek, Aaly Tokombaeva, 9/1a'),
        'company_phone_number': _('+996 (505) 054550'),
        'company_email': 'girlsforgirls@gmail.com',

        'forgot_your_password': _('Forgot your password?'),
        'we_received': _('We received a request to reset your password.'),
        'if_you_did_not': _('If you did not make this request, simply ignore this email.'),
        'if_you_did': _('If you did make this request just click the button below:'),
        'reset_password': _('RESET MY PASSWORD'),
        'if_you_did_not1': _('If you did not request to change your brand password,'),
        'do_not_have_to': _('you do not have to do anything. So that is easy.'),
    }

    # render email text
    email_html_message = render_to_string('email/user_reset_password.html', context)
    email_plaintext_message = render_to_string('email/user_reset_password.txt', context)

    msg = EmailMultiAlternatives(
        # title:
        _("Password Reset for Girls for Girls"),
        # message:
        email_plaintext_message,
        # from:
        settings.EMAIL_HOST,
        # to:
        [reset_password_token.user.email]
    )
    msg.attach_alternative(email_html_message, "text/html")
    msg.send()


class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number=None, email=None, password=None, **extra_fields):
        if not phone_number and not email:
            raise ValueError("Phone number or email must be specified for users.")
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
            raise ValueError("Superuser must have is_stuff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        if extra_fields.get("is_active") is not True:
            raise ValueError("Superuser must have is_active=True.")

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
        blank=True,
    )

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ()

    objects = CustomUserManager()

    region = models.ForeignKey('geoapi.Region', on_delete=models.SET_NULL, null=True, blank=True)
    district = models.ForeignKey('geoapi.District', on_delete=models.SET_NULL, null=True, blank=True)
    village = models.ForeignKey('geoapi.Village', on_delete=models.SET_NULL, null=True, blank=True)

    is_verified = models.BooleanField(default=False)

    def __str__(self) -> str:
        return "{}".format(self.username)
