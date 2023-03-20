from django.db import models


class LandingPage(models.Model):
    title = models.CharField(max_length=250)
    descriptions = models.TextField()
    statistics = models.TextField()
