from django.db import models

from parler.models import TranslatedFields

from forms.models import FormBase


class Trainings(FormBase):
    translations = TranslatedFields(
        title=models.CharField(max_length=255),
        description=models.TextField(blank=True, default=""),
        requirments=models.TextField(blank=True, default=""),
    )

    def __str__(self):
        return self.title


class TrainingsImage(models.Model):
    training = models.ForeignKey(
        Trainings, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(upload_to="images/trainings/")

    def __str__(self):
        return self.trainings.title
