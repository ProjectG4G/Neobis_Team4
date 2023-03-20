from django.db import models
from django.utils.translation import gettext_lazy as _
from users.models import User


class Mentorship(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    link = models.URLField()

    def __str__(self):
        return self.title


class MentorshipImage(models.Model):
    mentorship = models.ForeignKey(Mentorship, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='images/mentorship/')

    def __str__(self):
        return self.mentorship.title


class MentorshipApplications(models.Model):
    mentorship = models.ForeignKey(
        Mentorship,
        on_delete=models.CASCADE,
        verbose_name='Менторская программа')
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


class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    content = models.TextField()
    mentorship = models.ForeignKey(
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


class MentorshipQuestions(models.Model):
    mentorship = models.ForeignKey(
        Mentorship,
        on_delete=models.CASCADE,
        verbose_name='Ментрская программа')
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


class MentorProfile(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/mentor/')
    description = models.TextField()
