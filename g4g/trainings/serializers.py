from rest_framework.serializers import (
    ModelSerializer,
    ListField,
    ImageField,
)

from geoapi.models import (
    Region,
    District,
    Village,
)

from .models import (
    FAQ,
    Rating,
    Comment,
    Trainings,
    TrainingsImage,
    TrainingsApplications,
    TrainingsQuestions
)


class TrainingsImageSerializer(ModelSerializer):
    class Meta:
        model = TrainingsImage
        fields = "__all__"


class TrainingsSerializer(ModelSerializer):
    images = TrainingsImageSerializer(many=True, read_only=True)
    uploaded_images = ListField(
        child=ImageField(allow_empty_file=False, use_url=False),
        write_only=True,
        required=False
    )

    class Meta:
        model = Trainings
        fields = [
            'title',
            'header1',
            'header2',
            'header3',
            'header4',
            'body1',
            'body2',
            'body3',
            'body4',
            'images',
            'uploaded_images',
        ]

    def create(self, validated_data):
        uploaded_images = validated_data.pop("uploaded_images")

        training = Trainings.objects.create(**validated_data)

        for image in uploaded_images:
            TrainingsImage.objects.create(trainigs=training, image=image)

        return training


class TrainingCommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class TrainingRatingSerializer(ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'


class TrainingFAQSerializer(ModelSerializer):
    class Meta:
        model = FAQ
        fields = '__all__'


class TrainingApplicationsSerializer(ModelSerializer):
    class Meta:
        model = TrainingsApplications
        fields = '__all__'
        read_only_fields = ('user', 'is_accepted')

    def validate(self, attrs):
        region = attrs['region']
        district = attrs['district']
        village = attrs['village']

        if not Region.objects.filter(id=region.id).exists():
            raise serializers.ValidationError({'detail': 'Given region {} does not exist!'.format(region)})

        if not District.objects.filter(id=district.id).exists():
            raise serializers.ValidationError({'detail': 'Given district/city {} does not exist!'.format(district)})

        if village and not Village.objects.filter(id=village.id).exists():
            raise serializers.ValidationError({'detail': 'Given village {} does not exist!'.format(village)})

        if district.region != region:
            raise serializers.ValidationError(
                {'detail': 'Given district or city {} doesn\'t belong to region {}'.format(district, region)})

        if village and village.district != district:
            raise serializers.ValidationError(
                {'detail': 'Given village {} doesn\'t belong to district {}'.format(village, district)})

        return attrs

    def create(self, validated_data):
        request = self.context.get("request")

        validated_data['user'] = request.user

        application = TrainingsApplications.objects.create(**validated_data)

        return application


class TrainingQuestionsSerializer(ModelSerializer):
    class Meta:
        model = TrainingsQuestions
        fields = '__all__'
