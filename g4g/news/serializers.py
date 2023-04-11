from rest_framework import serializers

from .models import Tag, Article, ArticleImage

from parler_rest.serializers import TranslatableModelSerializer, TranslatedFieldsField


def upload_images(uploaded_images, article):
    for image in uploaded_images:
        ArticleImage.objects.create(image=image, article=article)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = (
            "id",
            "url",
            "name",
        )


class ArticleImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleImage
        fields = [
            "id",
            "url",
            "image",
            "article",
        ]


class ArticleParlerSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=Article)

    images = ArticleImageSerializer(many=True, read_only=True)

    uploaded_images = serializers.ListField(
        child=serializers.ImageField(allow_empty_file=True, required=False),
        write_only=True,
        required=False,
        allow_empty=True,
    )

    class Meta:
        model = Article
        fields = (
            "id",
            "url",
            "translations",
            "section",
            "tags",
            "images",
            "published",
            "edited",
        )

    def create(self, validated_data):
        uploaded_images = validated_data.pop("uploaded_image", [])

        article = super().create(validated_data)

        upload_images(uploaded_images=uploaded_images, article=article)

        return article

    def update(self, instance, validated_data):
        uploaded_images = validated_data.pop("uploaded_image", [])

        upload_images(uploaded_images=uploaded_images, article=instance)

        return super().update(instance, validated_data)
