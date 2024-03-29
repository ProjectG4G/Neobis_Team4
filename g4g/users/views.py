from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.shortcuts import redirect

from rest_framework import generics, status, filters

from rest_framework.decorators import action

from rest_framework.permissions import (
    AllowAny,
    IsAdminUser,
    IsAuthenticated,
)

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import RetrieveUpdateAPIView

from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken

from django_rest_passwordreset.views import (
    ResetPasswordRequestToken,
    ResetPasswordConfirm,
    ResetPasswordValidateToken,
)

from django_filters.rest_framework import DjangoFilterBackend

from drf_spectacular.utils import extend_schema

from mentorship.models import MentorProfile
from mentorship.serializers import MentorProfileSerializer

from .models import User
from .serializers import (
    RegisterSerializer,
    LoginPhoneSerializer,
    EmailVerificationSerializer,
    EmailVerificationConfirmSerializer,
    ChangePasswordSerializer,
    UserProfileUpdateSerializer,
    ModeratorSerializer,
    UserProfileUpdateMiniSerializer,
    LoginEmailSerializer,
)

from .verification import send_verification_email

from .permissions import IsProfileOwnerOrAdmin, IsSuperuser

from .filters import UserFilter

from decouple import config

from products.models import Cart


def send_verification(request, user):
    token = default_token_generator.make_token(user)
    verification_url = (
        request.build_absolute_uri(reverse("verification_confirm"))
        + f"?email={user.email}&token={token}"
    )
    send_verification_email(user, verification_url)


@extend_schema(tags=["Registration"])
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            user = serializer.save()

            cart = Cart.objects.create(user=user)
            cart.save()

            if config("VERIFICATION", default=False, cast=bool):
                if user.email and not user.is_verified:
                    send_verification(request, user)
                    return Response(
                        {
                            "detail": "User successfully created.",
                            "verification": "Verification email sent",
                        },
                        status=status.HTTP_201_CREATED,
                    )

            return Response(
                {"detail": "User successfully created."}, status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=["Login"])
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

        refresh["is_superuser"] = user.is_superuser
        refresh["is_staff"] = user.is_staff
        refresh["is_mentor"] = user.is_mentor

        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
        )


@extend_schema(tags=["Login"])
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

        refresh["is_superuser"] = user.is_superuser
        refresh["is_staff"] = user.is_staff
        refresh["is_mentor"] = user.is_mentor

        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
        )


@extend_schema(tags=["Email Verification"])
class EmailVerificationView(generics.GenericAPIView):
    serializer_class = EmailVerificationSerializer
    queryset = User.objects.all()

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            user = get_user_model().objects.get(email=email)

            if not user.is_verified:
                send_verification(request, user)
                return Response({"detail": "Verification email sent"})
            else:
                return Response(
                    {"detail": "Email already verified"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=["Email Verification"])
class EmailVerificationConfirmView(generics.GenericAPIView):
    serializer_class = EmailVerificationConfirmSerializer

    def get(self, request):
        email = request.query_params.get("email")
        token = request.query_params.get("token")
        try:
            user = get_user_model().objects.get(email=email)
            if not user.is_verified and default_token_generator.check_token(user, token):
                user.is_verified = True
                user.save()
                return redirect(to=config("EMAIL_VERIFICATION_REDIRECT_URL"))
            else:
                return Response(
                    {"detail": "Invalid email or token"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except get_user_model().DoesNotExist:
            return Response(
                {"detail": "Invalid email or token"}, status=status.HTTP_400_BAD_REQUEST
            )


@extend_schema(tags=["Password Change"])
class ChangePasswordView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            old_password = serializer.data.get("old_password")
            new_password = serializer.data.get("new_password")

            user = authenticate(
                email=request.user.email,
                phone_number=request.user.phone_number,
                password=old_password,
            )

            if user is not None:
                user.set_password(new_password)
                user.save()
                return Response(
                    {"message": "Password updated successfully."},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"message": "Invalid old password."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=["User Profile"])
class UserProfileView(ModelViewSet):
    queryset = User.objects.all()
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_class = UserFilter
    search_fields = (
        "email",
        "phone_number",
        "first_name",
        "last_name",
    )

    def get_serializer_class(self):
        if self.action == "create":
            return ModeratorSerializer
        elif self.request.user.is_staff:
            return UserProfileUpdateSerializer
        else:
            return UserProfileUpdateMiniSerializer

    def get_permissions(self):
        if self.action == "create":
            permission_classes = [IsAdminUser]
        elif self.action == "make_mentor":
            permission_classes = [IsAdminUser]
        elif self.action == "make_moderator":
            permission_classes = [IsSuperuser]
        else:
            permission_classes = [IsProfileOwnerOrAdmin]

        return [permission() for permission in permission_classes]

    @action(methods=["put"], detail=True)
    def make_moderator(self, request, pk=None):
        user = User.objects.get(pk=pk)

        user.is_staff = not user.is_staff

        user.save()

        if user.is_staff:
            return Response(
                {
                    "detail": "New Moderator Added",
                    "user": user.id,
                }
            )
        else:
            return Response(
                {
                    "detail": "Moderator Deleted",
                    "user": user.id,
                }
            )

    @action(methods=["put"], detail=True)
    def make_mentor(self, request, pk=None):
        user = User.objects.get(pk=pk)

        user.is_mentor = not user.is_mentor

        user.save()

        if user.is_mentor:
            mentor_profile = MentorProfile.objects.create(user=user)
            mentor_profile.save()

            return Response(
                {
                    "detail": "New Mentor Added",
                    "user": user.id,
                }
            )
        else:
            mentor_profile = MentorProfile.objects.get(user=user)
            mentor_profile.delete()

            return Response(
                {
                    "detail": "Mentor Deleted",
                    "user": user.id,
                }
            )


@extend_schema(tags=["User Stats"])
class UserRegisterStatisticView(APIView):
    def get(self, request, *args, **kwargs):
        year = kwargs["year"]
        data = {
            month: User.objects.filter(
                date_joined__month=month, date_joined__year=year
            ).count()
            for month in range(1, 13)
        }
        return Response(data)


# class UserByRegionStatisticView(APIView):
#


@extend_schema(tags=["Moderators"])
class ModeratorViewSet(ModelViewSet):
    queryset = User.objects.filter(is_staff=True)

    serializer_class = ModeratorSerializer

    permission_classes = [IsAdminUser]


@extend_schema(tags=["Mentor Profiles"])
class MentorProfileView(generics.RetrieveUpdateAPIView):
    queryset = MentorProfile.objects.all()
    serializer_class = MentorProfileSerializer

    def get_object(self):
        pk = self.kwargs["pk"]
        return MentorProfile.objects.get(user=pk)


@extend_schema(tags=["User Profile"])
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


@extend_schema(tags=["Password Reset"])
class ResetPasswordView(ResetPasswordRequestToken):
    pass


@extend_schema(tags=["Password Reset"])
class ResetPasswordConfirmView(ResetPasswordConfirm):
    pass


@extend_schema(tags=["Password Reset"])
class ResetPasswordValidateView(ResetPasswordValidateToken):
    pass
