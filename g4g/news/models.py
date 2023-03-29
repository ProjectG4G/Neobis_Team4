from django.db import models
from parler.models import TranslatableModel, TranslatedFields


class Tag(models.Model):
    name = models.CharField(max_length=32, null=False, blank=False, unique=True)

    def __str__(self):
        return self.name


class Article(TranslatableModel):
    translations = TranslatedFields(
        title=models.CharField(max_length=255, null=False, blank=False),
        content=models.TextField(null=False, blank=False),
    )
    # author = models.ForeignKey('users.User', on_delete=models.PROTECT)

    published = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)

    SECTIONS = (
        (1, 'Mentorship'),
        (2, 'Trainings'),
        (3, 'Shop'),
        (4, 'Video-blog'),
    )

    section = models.IntegerField(choices=SECTIONS, null=False)

    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.title


class ArticleImage(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to="articles")

    def __str__(self):
        return self.article.name
