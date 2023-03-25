from django.utils.translation import gettext_lazy as _
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings


def send_verification_email(user, verification_url, *args, **kwargs):
    # send an e-mail to the user

    # render email text

    msg = EmailMultiAlternatives(
        # title:
        _("Email verification for Girls for Girls"),
        # message:
        f"Hi {user.first_name}! \n Please verify you email with following link:\n{verification_url}",
        # from:
        settings.EMAIL_HOST,
        # to:
        [user.email]
    )

    # msg.attach_alternative(email_html_message, "text/html")

    msg.send()
