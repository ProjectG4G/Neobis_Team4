from rest_framework import serializers
from .models import VideoCategory, Video, Comment
from parler_rest.serializers import TranslatableModelSerializer, TranslatedFieldsField


class VideoCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoCategory
        fields = (
            "id",
            "name",
            "description",
            "image",
        )


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = (
            'id',
            'title',
            'description',
            'video_url',
        )


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = (
            'id',
            'content',
            'creation_at',
        )
