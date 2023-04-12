from django.db import models
from parler.models import TranslatableModel, TranslatedFields


class Tag(models.Model):
    objects = models.Manager()

    name = models.CharField(max_length=32, null=False, blank=False, unique=True)

    def __str__(self):
        return self.name


class Article(TranslatableModel):
    objects = models.Manager()

    translations = TranslatedFields(
        title=models.TextField(null=True, blank=True, default=""),
        content=models.TextField(null=True, blank=True, default=""),
    )
    # author = models.ForeignKey('users.User', on_delete=models.PROTECT)

    published = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)

    SECTIONS = (
        (1, "Mentorship"),
        (2, "Trainings"),
        (3, "Shop"),
        (4, "Video-blog"),
    )

    section = models.IntegerField(choices=SECTIONS, null=False)

    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return f"{self.id} - {self.title} - {self.published}"


class ArticleImage(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="images/articles")

    def __str__(self):
        return self.article.name
