# Generated by Django 4.1.7 on 2023-04-10 20:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("forms", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Mentee",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "program",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="forms.event"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="MentorProfile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("image", models.ImageField(null=True, upload_to="images/mentor/")),
                ("description", models.TextField(null=True)),
                ("mentees", models.ManyToManyField(blank=True, to="mentorship.mentee")),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="mentor",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
