from django.db import models
from django.utils.translation import gettext_lazy as _
from users.models import User


class Mentorship(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=250)
    content = models.TextField()
    link = models.SlugField()
    pictures = models.ImageField()

    def __str__(self):
        return self.name


class Applications(models.Model):
    mentorship_id = models.ForeignKey(
        Mentorship,
        on_delete=models.CASCADE,
        verbose_name='Заявки на менторскую программу')
    submit_date = models.DateTimeField()
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(
        max_length=12,
        null=True,
        unique=True,
    )

    email = models.EmailField(
        _("Email address"),
        max_length=255,
        null=True,
        unique=True,
        blank=True,
    )

    region = models.CharField(max_length=50)
    district = models.CharField(max_length=50)
    village = models.CharField(max_length=50)
    goals = models.TextField()
    expectations = models.TextField()
    resume = models.SlugField()
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Feedback(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    content = models.TextField()
    mentorship_id = models.ForeignKey(
        Mentorship,
        on_delete=models.CASCADE,
        verbose_name='отзыв о меноторской программе')
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content


class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()

    def __str__(self):
        return f'{self.question}'
