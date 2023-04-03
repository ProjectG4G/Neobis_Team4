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

    def __str__(self):
        return f"{self.title} - {self.formbase}"


class Question(models.Model):
    order = models.IntegerField(default=0)

    title = models.TextField()
    description = models.TextField()

    content = models.JSONField(
        blank=True,
        null=True,
    )

    required = models.BooleanField(default=False)

    form = models.ForeignKey(Form, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.order} - {self.title}"


class Application(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)

    STATUS = (
        (1, "Filling"),
        (2, "Submitted"),
        (3, "Declined"),
        (4, "Accepted"),
    )

    status = models.IntegerField(choices=STATUS, default=1)


class Response(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    application = models.ForeignKey(Application, on_delete=models.CASCADE)

    content = models.JSONField(
        blank=True,
        null=True,
    )
