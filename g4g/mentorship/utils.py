from django.db.models import Count

from rest_framework.response import Response

from .models import MentorProfile, Mentee


def accept_mentorship(self, application):
    if application.status == "accepted":
        return Response({"detail": "Application was already accepted!"})

    program = application.form.event

    mentee = Mentee.objects.create(
        program=application.form.event, user=application.user
    )

    mentor = (
        MentorProfile.objects.annotate(num_mentees=Count("mentees"))
        .filter(programs=program)
        .order_by("num_mentees")
    )[0]

    mentor.mentees.add(mentee)

    mentor.save()

    application.status = "accepted"

    application.save()

    return Response(
        {
            "detail": "Application accepted, Mentor {} was assigned to mentee {}!".format(
                mentor, mentee
            )
        }
    )
