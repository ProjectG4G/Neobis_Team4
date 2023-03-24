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


class LoginPhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['phone_number', 'password', ]


class LoginEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password', ]


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
            'url',
            'email',
            'phone_number',
            'first_name',
            'last_name',
            'profile_picture',
            'region',
            'district',
            'village',
            'is_verified',
            'is_staff',
            'is_mentor',
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
            'is_staff',
            'is_verified',
            'is_active',
        )

        read_only_fields = ('is_verified',)

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


class UserProfileUpdateMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'email',
            'phone_number',
            'first_name',
            'last_name',
            'profile_picture',
            'region',
            'district',
            'village',
        )

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


class ModeratorSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = (
            'email',
            'profile_picture',
            'first_name',
            'last_name',
            'region',
            'password',
            'is_staff',
        )

    def create(self, validated_data):
        password = validated_data.pop('password')

        user = User.objects.create_user(**validated_data)

        user.set_password(password)
        user.is_staff = True
        user.is_verified = True

        user.save()

        return user


class DummySerializer(serializers.Serializer):
    pass
