from django.contrib import admin

from parler.admin import TranslatableAdmin

from .models import ArticleImage, Article, Tag

admin.site.register(Article, TranslatableAdmin)
admin.site.register(Tag)
admin.site.register(ArticleImage)
