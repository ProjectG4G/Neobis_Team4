from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.db import models
from users.models import User


class Trainings(models.Model):
    title = models.CharField(max_length=255)

    header1 = models.TextField(blank=True, null=True)
    header2 = models.TextField(blank=True, null=True)
    header3 = models.TextField(blank=True, null=True)
    header4 = models.TextField(blank=True, null=True)

    body1 = models.TextField(blank=True, null=True)
    body2 = models.TextField(blank=True, null=True)
    body3 = models.TextField(blank=True, null=True)
    body4 = models.TextField(blank=True, null=True)

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
    why_you = models.CharField(max_length=250)


class TrainingsApplications(models.Model):
    training = models.ForeignKey(
        Trainings,
        on_delete=models.CASCADE,
        verbose_name='Тренинги')

    submit_date = models.DateTimeField(auto_now_add=True)

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

    can_attend = models.BooleanField()

    interested1 = models.TextField()

    why_you = models.TextField()

    interested2 = models.TextField()

    expectations = models.TextField()

    # resume = models.FileField(upload_to='files/mentorship/')

    about_training = models.CharField(max_length=255)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    is_accepted = models.BooleanField(default=False)

    def __str__(self):
        return self.training.title
