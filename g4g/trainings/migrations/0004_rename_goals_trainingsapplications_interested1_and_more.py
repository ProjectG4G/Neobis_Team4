# Generated by Django 4.1.5 on 2023-03-20 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trainings', '0003_remove_trainings_description_remove_trainings_image_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='trainingsapplications',
            old_name='goals',
            new_name='interested1',
        ),
        migrations.RenameField(
            model_name='trainingsapplications',
            old_name='mentorship',
            new_name='training',
        ),
        migrations.RemoveField(
            model_name='trainingsapplications',
            name='resume',
        ),
        migrations.AddField(
            model_name='trainingsapplications',
            name='about_training',
            field=models.CharField(default=None, max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='trainingsapplications',
            name='can_attend',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='trainingsapplications',
            name='interested2',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='trainingsapplications',
            name='is_accepted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='trainingsapplications',
            name='why_you',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='trainingsquestions',
            name='why_you',
            field=models.CharField(default='', max_length=250),
            preserve_default=False,
        ),
    ]