from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.shortcuts import redirect

from rest_framework import generics, status, filters, views

from rest_framework.decorators import action

from rest_framework.permissions import (
    AllowAny,
    IsAuthenticatedOrReadOnly,
    IsAdminUser,
    IsAuthenticated,
)

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import RetrieveUpdateAPIView

from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken

from django_filters.rest_framework import DjangoFilterBackend

from mentorship.models import MentorProfile
from mentorship.serializers import MentorProfileSerializer

from .models import User
from .serializers import (
    RegisterSerializer,
    LoginPhoneSerializer,
    EmailVerificationSerializer,
    EmailVerificationConfirmSerializer,
    ChangePasswordSerializer,
    UserProfileSerializer,
    UserProfileUpdateSerializer,
    ModeratorSerializer,
    DummySerializer,
    UserProfileUpdateMiniSerializer,
    LoginEmailSerializer,
)

from .verification import send_verification_email

from .permissions import IsProfileOwnerOrAdmin

from .filters import UserFilter

from decouple import config


def send_verification(request, user):
    token = default_token_generator.make_token(user)
    verification_url = request.build_absolute_uri(
        reverse('verification_confirm')
    ) + f'?email={user.email}&token={token}'
    send_verification_email(user, verification_url)


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            user = serializer.save()

            if config("VERIFICATION", default=False, cast=bool):
                if user.email and not user.is_verified:
                    send_verification(request, user)
                    return Response({"detail": "User successfully created.", 'verification': 'Verification email sent'},
                                    status=status.HTTP_201_CREATED)

            return Response({"detail": "User successfully created."},
                            status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginPhoneView(generics.GenericAPIView):
    serializer_class = LoginPhoneSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        phone_number = request.data["phone_number"]
        password = request.data["password"]
        user = User.objects.filter(phone_number=phone_number).first()

        if user is None:
            raise AuthenticationFailed("User not found!")

        if not user.check_password(password):
            raise AuthenticationFailed("Incorrect password!")

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
        )


class LoginEmailView(generics.GenericAPIView):
    serializer_class = LoginEmailSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        email = request.data["email"]
        password = request.data["password"]
        user = User.objects.filter(email=email).first()
        if config("VERIFICATION", default=False, cast=bool):
            if not user.is_verified:
                raise AuthenticationFailed("User is not verified!")
        if user is None:
            raise AuthenticationFailed("User not found!")

        if not user.check_password(password):
            raise AuthenticationFailed("Incorrect password!")

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
        )


class EmailVerificationView(generics.GenericAPIView):
    serializer_class = EmailVerificationSerializer
    queryset = User.objects.all()

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = get_user_model().objects.get(email=email)

            if not user.is_verified:
                send_verification(request, user)
                return Response({'detail': 'Verification email sent'})
            else:
                return Response({'detail': 'Email already verified'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmailVerificationConfirmView(generics.GenericAPIView):
    serializer_class = EmailVerificationConfirmSerializer

    def get(self, request):
        email = request.query_params.get('email')
        token = request.query_params.get('token')
        try:
            user = get_user_model().objects.get(email=email)
            if not user.is_verified and default_token_generator.check_token(user, token):
                user.is_verified = True
                user.save()
                # TODO setup valid url
                return redirect(to='http://localhost:3000/login/')
            else:
                return Response({'detail': 'Invalid email or token'}, status=status.HTTP_400_BAD_REQUEST)
        except get_user_model().DoesNotExist:
            return Response({'detail': 'Invalid email or token'}, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            old_password = serializer.data.get("old_password")
            new_password = serializer.data.get("new_password")

            user = authenticate(email=request.user.email, phone_number=request.user.phone_number, password=old_password)

            if user is not None:
                user.set_password(new_password)
                user.save()
                return Response({"message": "Password updated successfully."}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Invalid old password."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(ModelViewSet):
    queryset = User.objects.all()
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_class = UserFilter
    search_fields = ('email', 'phone_number', 'first_name', 'last_name',)

    permission_classes = (IsProfileOwnerOrAdmin,)

    def get_serializer_class(self):
        if self.action == 'list':
            return UserProfileSerializer
        if self.action == 'create':
            return ModeratorSerializer
        if self.request.user.is_staff:
            return UserProfileUpdateSerializer
        else:
            return UserProfileUpdateMiniSerializer

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsProfileOwnerOrAdmin]

        return [permission() for permission in permission_classes]

    @action(methods=['put'], detail=True)
    def make_moderator(self, request, pk=None):
        user = User.objects.get(pk=pk)

        user.is_staff = not user.is_staff

        user.save()

        if user.is_staff:
            return Response({
                'detail': 'New Moderator Added',
                'user': user.id,
            })
        else:
            return Response({
                'detail': 'Moderator Deleted',
                'user': user.id,
            })

    @action(methods=['put'], detail=True)
    def make_mentor(self, request, pk=None):
        user = User.objects.get(pk=pk)

        user.is_mentor = not user.is_mentor

        user.save()

        if user.is_mentor:

            mentor_profile = MentorProfile.objects.create(user=user)
            mentor_profile.save()

            return Response({
                'detail': 'New Mentor Added',
                'user': user.id,
            })
        else:
            mentor_profile = MentorProfile.objects.get(user=user)
            mentor_profile.delete()

            return Response({
                'detail': 'Mentor Deleted',
                'user': user.id,
            })


class UserRegisterStatisticView(APIView):
    def get(self, request, *args, **kwargs):
        year = kwargs['year']
        data = {
            month: User.objects.filter(date_joined__month=month, date_joined__year=year).count() for month in
            range(1, 13)
        }
        return Response(data)


# class UserByRegionStatisticView(APIView):
#


class ModeratorViewSet(ModelViewSet):
    queryset = User.objects.filter(is_staff=True)

    serializer_class = ModeratorSerializer

    permission_classes = [IsAdminUser]


class MentorProfileView(generics.RetrieveUpdateAPIView):
    queryset = MentorProfile.objects.all()
    serializer_class = MentorProfileSerializer

    def get_object(self):
        pk = self.kwargs['pk']
        return MentorProfile.objects.get(user=pk)


class UserProfileRetrieveView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserProfileUpdateMiniSerializer

    def get_object(self):
        user = self.request.user
        return user

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
