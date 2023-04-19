from rest_framework.response import Response

from .models import Applicant


def accept_training(self, application):
    if application.status == "accepted":
        return Response({"detail": "Application was already accepted!"})

    application.status = "accepted"
    application.save()

    Applicant.objects.create(training=application.form.event, user=application.user)

    return Response({"detail": "Application accepted!"})
