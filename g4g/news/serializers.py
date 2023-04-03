from rest_framework import serializers

from .models import Tag, Article, ArticleImage

from parler_rest.serializers import TranslatableModelSerializer, TranslatedFieldsField


def get_language(self):
    return self.context["request"].headers.get("Accept-Language")


def switch_language(lang):
    if lang == "ky":
        return "ru"
    elif lang == "ru":
        return "ky"


def upload_images(uploaded_images, article):
    for image in uploaded_images:
        ArticleImage.objects.create(image=image, article=article)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name"]


class ArticleImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleImage
        fields = [
            "url",
            "id",
            "image",
            "article",
        ]


class ArticleReadOnlySerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    content = serializers.SerializerMethodField()
    lang = serializers.SerializerMethodField()

    images = ArticleImageSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Article
        fields = (
            "id",
            "url",
            "lang",
            "title",
            "content",
            "images",
            "tags",
            "section",
            "published",
            "edited",
        )

    def get_lang(self, obj):
        return get_language(self)

    def get_title(self, obj):
        obj.set_current_language(get_language(self))
        return obj.title

    def get_content(self, obj):
        obj.set_current_language(get_language(self))
        return obj.content


class ArticleCreateSerializer(serializers.ModelSerializer):
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(allow_empty_file=True, required=False),
        write_only=True,
        required=False,
        allow_empty=True,
    )

    title = serializers.CharField()
    content = serializers.CharField()

    class Meta:
        model = Article
        fields = (
            "title",
            "content",
            "uploaded_images",
            "section",
        )

    def create(self, validated_data):
        language = get_language(self)

        images = validated_data.pop("uploaded_images", [])

        article = Article.objects.language(language).create(**validated_data)

        article.set_current_language(switch_language(language))

        article.title = ""
        article.content = ""

        article.save()

        upload_images(images, article=article)

        article.set_current_language(language)

        return article


class ArticlePreCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ("section",)

    def create(self, validated_data):
        validated_data["title"] = ""
        validated_data["content"] = ""
        article = Article.objects.language("ky").create(**validated_data)

        article.set_current_language("ru")

        article.title = ""
        article.content = ""

        article.save()

        return article


class ArticleUpdateSerializer(serializers.Serializer):
    title = serializers.CharField(write_only=True, required=True)
    content = serializers.CharField(write_only=True, required=True)

    uploaded_images = serializers.ListField(
        child=serializers.ImageField(required=False, allow_empty_file=True),
        write_only=True,
        required=False,
    )

    def update(self, instance, validated_data):
        uploaded_images = validated_data.pop("uploaded_images", [])

        instance.set_current_language(get_language(self))

        instance.title = validated_data["title"]
        instance.content = validated_data["content"]

        instance.save()

        upload_images(uploaded_images, article=instance)

        return instance


class ArticleParlerSerializer(TranslatableModelSerializer):
    images = ArticleImageSerializer(many=True, read_only=True)
    translations = TranslatedFieldsField(shared_model=Article)

    class Meta:
        model = Article
        fields = (
            "id",
            "translations",
            "section",
            "tags",
            "images",
            "published",
            "edited",
        )
