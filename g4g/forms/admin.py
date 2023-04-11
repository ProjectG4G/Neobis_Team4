from django.contrib import admin
from parler.admin import TranslatableAdmin

from .models import (
    Application,
    Event,
    Question,
    Response,
    Form,
    Choice,
    EventImage,
)

admin.site.register(Event, TranslatableAdmin)
admin.site.register(Form, TranslatableAdmin)
admin.site.register(Question)
admin.site.register(Application)
admin.site.register(Response)
admin.site.register(Choice)
admin.site.register(EventImage)
