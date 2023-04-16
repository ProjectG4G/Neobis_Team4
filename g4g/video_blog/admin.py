from django.contrib import admin
from parler.admin import TranslatableAdmin
from .models import Playlist, Video, Comment, RecentlyWatched

admin.site.register(Playlist, TranslatableAdmin)
admin.site.register(Video)
admin.site.register(Comment)
admin.site.register(RecentlyWatched)
