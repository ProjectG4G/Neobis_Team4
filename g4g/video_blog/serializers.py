from rest_framework import serializers
from .models import Playlist, Video, Comment, RecentlyWatched
from parler_rest.serializers import TranslatableModelSerializer, TranslatedFieldsField


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = (
            "id",
            "url",
            "playlist",
            "title",
            "description",
            "video_url",
        )


class PlaylistSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=Playlist, required=False)
    videos = VideoSerializer(many=True, read_only=True)

    class Meta:
        model = Playlist
        fields = (
            "id",
            "url",
            "translations",
            "image",
            "videos",
        )


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = (
            "id",
            "url",
            "content",
            "video",
            "created_at",
        )


class RecentlyWatchedSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecentlyWatched
        fields = (
            "id",
            "url",
            "user",
            "video",
            "timestamp",
        )
        read_only_fields = ("user",)

    def create(self, validated_data):
        user = self.context['request'].user
        video = validated_data['video']
        recently_watched = RecentlyWatched.objects.create(user=user, video=video)
        recently_watched.save()
        return recently_watched
