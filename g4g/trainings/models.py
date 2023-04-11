from django.db import models


class Applicants(models.Model):
    training = models.ForeignKey("forms.Event", on_delete=models.CASCADE)
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
