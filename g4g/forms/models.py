from django.db import models
from parler.models import TranslatableModel, TranslatedFields


class FormBase(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)


class Form(TranslatableModel):
    translations = TranslatedFields(
        title=models.TextField(blank=True, default=""),
        description=models.TextField(blank=True, default=""),
    )

    created = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)

    active = models.BooleanField(default=False)

    formbase = models.ForeignKey(FormBase, on_delete=models.CASCADE)


class Question(models.Model):
    order = models.IntegerField(default=0)

    title = (models.TextField(blank=True, default=""),)
    description = (models.TextField(blank=True, default=""),)

    content = models.JSONField(
        blank=True,
        null=True,
    )

    required = models.BooleanField(default=False)

    form = models.ForeignKey(Form, on_delete=models.CASCADE)
