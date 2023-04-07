from django.db import models

from parler.models import TranslatableModel, TranslatedFields

from forms.models import FormBase


class Mentorship(FormBase):
    translation = TranslatedFields(
        title=models.TextField(null=True, blanck=True, default=""),
        description=models.TextField(null=True, blank=True, default=""),
        requirements=models.TextField(null=True, blank=True, default=""),
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class MentorshipImage(models.Model):
    mentorship = models.ForeignKey(
        Mentorship, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(upload_to="images/mentorship/")

    def __str__(self):
        return self.mentorship.title


class MentorProfile(models.Model):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="images/mentor/", null=True)
    description = models.TextField(null=True)
