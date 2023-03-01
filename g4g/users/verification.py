from django.utils.translation import gettext_lazy as _
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings


def send_verification_email(user, verification_url, *args, **kwargs):
    # send an e-mail to the user

    context = {
        'site_name': 'Girls for Girls',

        'email': user.email,
        'verification_url': verification_url,

        'company_address': _('Bishkek, Aaly Tokombaeva, 9/1a'),
        'company_phone_number': '+996 (505) 054550',
        'company_email': 'girlsforgirls@gmail.com',

        'hi': _('Hi, ') + '{}'.format(user.first_name),
        'you_registered': _('You registered an account on Girls for Girls.'),
        'we_need': _('We need a little more information to complete your registration, '),
        'including': _('including a confirmation of your email address.'),
        'verify_below': _('Please verify your email just clicking the button below:'),
        'verify': _('VERIFY MY EMAIL'),
        'glad': _('We’re glad you’re here!'),
        'team_g4g': _('The Girls for Girls team.'),
    }

    # render email text
    email_html_message = render_to_string('email/user_email_verification.html', context)
    email_plaintext_message = render_to_string('email/user_email_verification.txt', context)

    msg = EmailMultiAlternatives(
        # title:
        _("Email verification for Girls for Girls"),
        # message:
        email_plaintext_message,
        # from:
        settings.EMAIL_HOST,
        # to:
        [user.email]
    )
    msg.attach_alternative(email_html_message, "text/html")
    msg.send()
