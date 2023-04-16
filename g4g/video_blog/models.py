from django.conf import settings
from django.db import models
from parler.models import TranslatableModel, TranslatedFields


class Playlist(TranslatableModel):
    translations = TranslatedFields(
        name=models.CharField(max_length=255, blank=True),
        description=models.TextField(blank=True),
    )
    image = models.ImageField(upload_to="images/playlist/", null=True)

    def __str__(self):
        return self.name


class Video(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    video_url = models.URLField()
    playlist = models.ForeignKey(
        Playlist, on_delete=models.CASCADE, related_name="videos"
    )

    def __str__(self):
        return self.title


class Comment(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, null=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.last_name} - {self.video.title}"


class RecentlyWatched(models.Model):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
