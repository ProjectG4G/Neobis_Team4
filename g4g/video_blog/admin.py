from django.contrib import admin
from .models import VideoCategory, Video, Comment

admin.site.register(VideoCategory)
admin.site.register(Video)
admin.site.register(Comment)
