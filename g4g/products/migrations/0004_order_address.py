# Generated by Django 4.1.7 on 2023-04-21 13:57

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0003_alter_productimage_options"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="address",
            field=models.CharField(default="", max_length=255, verbose_name="Адрес"),
        ),
    ]
