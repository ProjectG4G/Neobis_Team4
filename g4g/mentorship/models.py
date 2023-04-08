from django.db import models


class MentorProfile(models.Model):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="images/mentor/", null=True)
    description = models.TextField(null=True)
