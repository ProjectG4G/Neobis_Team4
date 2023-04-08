from django.contrib import admin
from parler.admin import TranslatableAdmin

from .models import Application, Question, Response, Form, FormBase

admin.site.register(FormBase)
admin.site.register(Form, TranslatableAdmin)
admin.site.register(Question)
admin.site.register(Application)
admin.site.register(Response)
