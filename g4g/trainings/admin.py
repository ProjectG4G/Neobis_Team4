from django.contrib import admin

from parler.admin import TranslatableAdmin

from .models import Trainings

admin.site.register(Trainings, TranslatableAdmin)
