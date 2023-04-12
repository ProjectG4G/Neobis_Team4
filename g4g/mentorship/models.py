from django.db import models


class Mentee(models.Model):
    objects = models.Manager()

    program = models.ForeignKey("forms.Event", on_delete=models.CASCADE)
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class MentorProfile(models.Model):
    objects = models.Manager()

    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="mentor"
    )
    image = models.ImageField(upload_to="images/mentor/", null=True)
    description = models.TextField(null=True)
    mentees = models.ManyToManyField("Mentee", blank=True)
