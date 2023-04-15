from django.conf import settings
from django.db import models


class VideoCategory(models.Model):
    name = models.CharField(max_length=255, blank=True)
    description = models.TextField()
    image = models.ImageField(upload_to="images/video_category/", null=True)

    def __str__(self):
        return self.name


class Video(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField()
    video_url = models.URLField()
    category = models.ForeignKey(
        VideoCategory, on_delete=models.CASCADE, related_name="category"
    )

    def __str__(self):
        return self.title


class Comment(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, null=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.video.title}"
