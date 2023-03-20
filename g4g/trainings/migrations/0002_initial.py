# Generated by Django 4.1.5 on 2023-03-20 10:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('trainings', '0001_initial'),
        ('geoapi', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='trainingsapplications',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='trainingsapplications',
            name='village',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='geoapi.village'),
        ),
        migrations.AddField(
            model_name='rating',
            name='trainings',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='trainings.trainings'),
        ),
        migrations.AddField(
            model_name='rating',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comment',
            name='replies',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='trainings.comment'),
        ),
        migrations.AddField(
            model_name='comment',
            name='training',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='trainings.trainings'),
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
