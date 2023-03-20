# Generated by Django 4.1.5 on 2023-03-20 10:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('geoapi', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FAQ',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=255)),
                ('answer', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('content', models.TextField()),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='MentorProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='images/mentor/')),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Mentorship',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(max_length=255)),
                ('content', models.TextField()),
                ('link', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='MentorshipQuestions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('phone_number', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=50)),
                ('region', models.CharField(max_length=250)),
                ('district', models.CharField(max_length=250)),
                ('village', models.CharField(max_length=250)),
                ('goals', models.TextField()),
                ('expectations', models.TextField()),
                ('resume', models.CharField(max_length=250)),
                ('mentorship', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mentorship.mentorship', verbose_name='Ментрская программа')),
            ],
        ),
        migrations.CreateModel(
            name='MentorshipImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='images/mentorship/')),
                ('mentorship', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='mentorship.mentorship')),
            ],
        ),
        migrations.CreateModel(
            name='MentorshipApplications',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('submit_date', models.DateTimeField()),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('phone_number', models.CharField(max_length=12, null=True, unique=True)),
                ('email', models.EmailField(blank=True, max_length=255, null=True, unique=True, verbose_name='Email address')),
                ('goals', models.TextField()),
                ('expectations', models.TextField()),
                ('resume', models.FileField(upload_to='files/mentorship/')),
                ('district', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='geoapi.district')),
                ('mentorship', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mentorship.mentorship', verbose_name='Менторская программа')),
                ('region', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='geoapi.region')),
            ],
        ),
    ]