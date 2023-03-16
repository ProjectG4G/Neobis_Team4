from rest_framework import serializers

from .models import Tag, Article, ArticlesImage


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


class ArticlesImageSerializers(serializers.ModelSerializer):
    class Meta:
        model = ArticlesImage
        fields = "__all__"


class ArticleSerializer(serializers.ModelSerializer):
    images = ArticlesImageSerializers(many=True, read_only=True)
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(allow_empty_file=False, use_url=False),
        write_only=True
    )

    class Meta:
        model = Article
        fields = [
            'id',
            'title',
            'content',
            'section',
            'images',
            'uploaded_images',
            'published',
            'edited',
        ]

    def create(self, validated_data):
        uploaded_images = validated_data.pop("uploaded_images")
        article = Article.objects.create(**validated_data)

        for image in uploaded_images:
            ArticlesImage.objects.create(article=article, image=image)

        return article
