from rest_framework import serializers
from .models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from geoapi.models import Region, District
from geoapi.utils import extract


# from geoapi.serializers import RegionSerializer


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        allow_blank=True,
        required=False,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    phone_number = serializers.CharField(
        required=False,
        allow_blank=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('email', 'phone_number', 'password', 'password2', 'first_name', 'last_name', 'region', 'district',)
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({'password': 'Password fields did not match.'})

        region = attrs['region']
        district = attrs['district']

        if not Region.objects.filter(id=region.id).exists():
            raise serializers.ValidationError({'detail': 'Given region {} does not exist!'.format(region)})

        if not District.objects.filter(id=district.id).exists():
            raise serializers.ValidationError({'detail': 'Given district/city {} does not exist!'.format(district)})

        if district.region != region:
            raise serializers.ValidationError(
                {'detail': 'Given district or city {} doesn\'t belong to region {}'.format(district, region)})

        return attrs

    @staticmethod
    def none_if_empty(obj):
        return obj if obj else None

    @staticmethod
    def obj_by_name(model, value):
        if model.objects.filter(name=value).exists():
            return model.objects.get(name=value)
        return None

    def create(self, validated_data):
        email = self.none_if_empty(validated_data['email'])
        phone_number = self.none_if_empty(validated_data['phone_number'])

        if not email and not phone_number:
            raise serializers.ValidationError({'detail': 'Email or Phone number must be specified.'})

        user = User.objects.create(
            email=email,
            phone_number=phone_number,
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            region=validated_data['region'],
            district=validated_data['district'],
        )

        user.set_password(validated_data['password'])
        user.save()

        return user


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['phone_number', 'password', ]


class EmailVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField(
        required=True,
        allow_blank=False,
    )


class EmailVerificationConfirmSerializer(serializers.Serializer):
    pass


class ChangePasswordSerializer(serializers.Serializer):
    model = User
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'phone_number',
            'first_name',
            'last_name',
            'profile_picture',
            'region',
            'district',
            'village',
            'is_verified',
        )


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'phone_number',
            'first_name',
            'last_name',
            'profile_picture',
            'region',
            'district',
            'village',
            'is_verified',
        )

        depth = 1
