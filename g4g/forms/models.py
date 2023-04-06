from django.db import models

from parler.models import TranslatableModel, TranslatedFields


class FormBase(TranslatableModel):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Form(TranslatableModel):
    translations = TranslatedFields(
        title=models.TextField(blank=True, default=""),
        description=models.TextField(blank=True, default=""),
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    active = models.BooleanField(default=False)

    formbase = models.ForeignKey(FormBase, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} - {self.formbase}"


class Question(models.Model):
    order = models.IntegerField(default=0)

    title = models.TextField()
    description = models.TextField()

    question_type = models.CharField(
        max_length=255,
        choices=(
            ("text", "Text"),
            ("paragraph", "Paragraph"),
            ("multiple_choice", "Multiple Choice"),
            ("checkbox", "Checkbox"),
        ),
    )

    required = models.BooleanField(default=False)

    form = models.ForeignKey(Form, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.order} - {self.title}"


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    choice_text = models.CharField(max_length=255)


class Application(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    STATUS = (
        ("filling", "Filling"),
        ("submitted", "Submitted"),
        ("declined", "Declined"),
        ("accepted", "Accepted"),
    )

    user = models.ForeignKey("users.User", on_delete=models.CASCADE)

    status = models.CharField(choices=STATUS, default="filling", max_length=255)


class Response(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    application = models.ForeignKey(Application, on_delete=models.CASCADE)

    response_choices = models.ManyToManyField(Choice, blank=True)

    response_text = models.TextField(blank=True, null=True)
