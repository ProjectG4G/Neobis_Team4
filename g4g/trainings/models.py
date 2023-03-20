from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.db import models
from users.models import User


class Trainings(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    url = models.CharField(max_length=255)
    image = models.ImageField(upload_to="images/")

    def __str__(self):
        return self.title


class Comment(models.Model):
    training = models.ForeignKey(Trainings, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    content = models.TextField()
    replies = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content


class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()

    def __str__(self):
        return f'{self.question}'


class Rating(models.Model):
    rates = ((1, 1), (2, 2), (3, 3), (4, 4), (5, 5))
    trainings = models.ForeignKey(Trainings, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    rating = models.PositiveSmallIntegerField(choices=rates, default=1)


class TrainingsImage(models.Model):
    trainings = models.ForeignKey(Trainings, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='images/trainings/')

    def __str__(self):
        return self.trainings.title


class TrainingsQuestions(models.Model):
    trainings = models.ForeignKey(
        Trainings,
        on_delete=models.CASCADE,
        verbose_name='Тренинги')
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    region = models.CharField(max_length=250)
    district = models.CharField(max_length=250)
    village = models.CharField(max_length=250)
    goals = models.TextField()
    expectations = models.TextField()
    resume = models.CharField(max_length=250)


class TrainingsApplications(models.Model):
    mentorship = models.ForeignKey(
        Trainings,
        on_delete=models.CASCADE,
        verbose_name='Тренинги')
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

    region = models.ForeignKey('geoapi.Region', on_delete=models.SET_NULL, null=True)
    district = models.ForeignKey('geoapi.District', on_delete=models.SET_NULL, null=True)
    village = models.ForeignKey('geoapi.Village', on_delete=models.SET_NULL, null=True)
    goals = models.TextField()
    expectations = models.TextField()
    resume = models.FileField(upload_to='files/mentorship/')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.mentorship.title

