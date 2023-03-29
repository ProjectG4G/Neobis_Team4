from rest_framework import serializers

from .models import Tag, Article, ArticleImage


# from parler_rest.serializers import TranslatableModelSerializer, TranslatedFieldsField


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


class ArticleImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleImage
        fields = [
            'url',
            'id',
            'image',
            'article',
        ]


class ArticleSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    added_tags = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False,
    )

    images = ArticleImageSerializer(many=True, read_only=True)
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(allow_empty_file=False, use_url=False),
        write_only=True,
        required=False
    )

    title = serializers.SerializerMethodField('get_title')
    content = serializers.SerializerMethodField('get_title')

    class Meta:
        model = Article
        fields = [
            'id',
            'section',
            'images',
            'uploaded_images',
            'added_tags',
            'published',
            'edited',
            'tags',
        ]

    def create(self, validated_data):
        uploaded_images = validated_data.pop("uploaded_images")
        added_tags = validated_data.pop("added_tags")

        for image in uploaded_images:
            ArticleImage.objects.create(article=article, image=image)

        for tag in added_tags:
            article.tags.add(Tag.objects.get(id=tag))

        return article


class ArticleContentSerializer(serializers.ModelSerializer):
    pass


class AddTagSerializer(serializers.Serializer):
    class Meta:
        model = Tag
        fields = ['id']


class ArticleAddTagsSerializer(serializers.Serializer):
    added_tags = serializers.ListField(
        child=AddTagSerializer(),
        write_only=True,
        required=False,
    )

    def update(self, instance, validated_data):
        added_tags = validated_data['added_tags']
        for tag in added_tags:
            print(tag)
            instance.tags.add(Tag.objects.get(id=tag))
