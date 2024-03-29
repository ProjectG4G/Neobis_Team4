from django.db import models

from parler.models import TranslatableModel, TranslatedFields
from parler.managers import TranslatableManager


class Event(TranslatableModel):
    objects = TranslatableManager()

    translations = TranslatedFields(
        title=models.CharField(max_length=255),
        description=models.TextField(blank=True, default=""),
        requirements=models.TextField(blank=True, default=""),
    )

    type = models.CharField(
        choices=(
            ("mentorship", "Mentorship Programs"),
            ("training", "Trainings"),
            ("no_event", "No Event"),
        ),
        max_length=255,
    )

    event_date = models.DateTimeField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class EventImage(models.Model):
    objects = models.Manager()

    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="images/events/")

    def __str__(self):
        return self.event.title


class Form(TranslatableModel):
    objects = TranslatableManager()

    translations = TranslatedFields(
        title=models.TextField(blank=True, default=""),
        description=models.TextField(blank=True, default=""),
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    active = models.BooleanField(default=False)

    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="form")

    def __str__(self):
        return f"{self.title} - {self.event}"


class Question(models.Model):
    objects = models.Manager()

    order = models.IntegerField(default=0)

    title = models.TextField()
    description = models.TextField(blank=True)

    question_type = models.CharField(
        max_length=255,
        choices=(
            ("text", "Text"),
            ("paragraph", "Paragraph"),
            ("multiple_choice", "Multiple Choice"),
            ("checkbox", "Checkbox"),
            ("file", "File"),
        ),
    )

    required = models.BooleanField(default=False)

    form = models.ForeignKey(Form, on_delete=models.CASCADE, related_name="questions")

    def __str__(self):
        return f"{self.title}"


class Choice(models.Model):
    objects = models.Manager()

    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="choices"
    )

    choice_text = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.choice_text}"


class Application(models.Model):
    objects = models.Manager()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    STATUS = (
        ("filling", "Filling"),
        ("submitted", "Submitted"),
        ("declined", "Declined"),
        ("accepted", "Accepted"),
    )

    form = models.ForeignKey(Form, on_delete=models.CASCADE)

    user = models.ForeignKey("users.User", on_delete=models.CASCADE)

    status = models.CharField(choices=STATUS, default="filling", max_length=255)

    def __str__(self):
        return f"{self.form.title} {self.user}"


class Response(models.Model):
    objects = models.Manager()

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    application = models.ForeignKey(
        Application, on_delete=models.CASCADE, related_name="responses"
    )

    response_choices = models.ManyToManyField(Choice, blank=True)

    response_text = models.TextField(blank=True, null=True)

    response_file = models.FileField(blank=True, null=True, upload_to="files/forms/")
