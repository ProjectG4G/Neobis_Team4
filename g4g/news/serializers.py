from rest_framework import serializers

from .models import Tag, Article, ArticlesImage
from parler_rest.serializers import TranslatableModelSerializer, TranslatedFieldsField


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


class ArticlesImageSerializers(TranslatableModelSerializer):
    class Meta:
        model = ArticlesImage
        fields = "__all__"


class ArticleSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    added_tags = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False,
    )

    images = ArticlesImageSerializers(many=True, read_only=True)
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(allow_empty_file=False, use_url=False),
        write_only=True,
        required=False
    )

    translations = TranslatedFieldsField(shared_model=Article)

    class Meta:
        model = Article
        fields = [
            'id',
            'translations',
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
        translations = validated_data.pop("translations")

        ky = translations['ky']
        ru = translations['ru']

        article = Article.objects.create(**validated_data)
        article.set_current_language('ky')

        article.title = ky['title']
        article.content = ky['content']

        article.set_current_language('ru')
        article.title = ru['title']
        article.content = ru['content']

        article.save()

        for image in uploaded_images:
            ArticlesImage.objects.create(article=article, image=image)

        for tag in added_tags:
            article.tags.add(Tag.objects.get(id=tag))

        return article


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


class ArticleContentSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField(read_only=True)
    content = serializers.SerializerMethodField(read_only=True)

    edit_title = serializers.CharField(max_length=255, write_only=True)
    edit_content = serializers.TextField(write_only=True)

    class Meta:
        model = Article
        fields = ['get_title', 'get_context']

    def update(self, instance, validated_data):
        pass