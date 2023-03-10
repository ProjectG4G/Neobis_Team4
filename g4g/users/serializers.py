from rest_framework import serializers
from .models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from geoapi.models import Region, District
from geoapi.utils import extract


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

    region = serializers.CharField(max_length=64)
    district = serializers.CharField(max_length=64)

    class Meta:
        model = User
        fields = ('email', 'phone_number', 'password', 'password2', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({'password': 'Password fields did not match.'})

        if not Region.objects.filter(name=attrs['region']).exist():
            raise serializers.ValidationError({'region': 'Given region {} does not exist!'.format(attrs['region'])})

        if not District.objects.filter(
                name=extract(attrs['district']).exist() and City.objects.filter(name=extract(attrs['district']))):
            raise serializers.ValidationError(
                {'region': 'Given district/city {} does not exist!'.format(attrs['region'])})

        return attrs

    @staticmethod
    def none_if_empty(obj):
        return obj if obj else None

    def create(self, validated_data):
        email = self.none_if_empty(validated_data['email'])
        phone_number = self.none_if_empty(validated_data['phone_number'])

        if not email and not phone_number:
            raise serializers.ValidationError({'Credentials': 'Email or Phone number must be specified.'})

        region = Region.objects.get(name=validated_data['region'])
        district = Region.objects.get(name=validated_data['district'])

        user = User.objects.create(
            email=email,
            phone_number=phone_number,
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['phone_number', 'password', ]


class EmailVerifactionSerializer(serializers.Serializer):
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
