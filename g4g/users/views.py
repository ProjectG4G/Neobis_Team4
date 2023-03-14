from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse

from rest_framework import generics, status

from rest_framework.permissions import (
    AllowAny,
    IsAuthenticatedOrReadOnly,
    IsAdminUser,
    IsAuthenticated,
)

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    EmailVerifactionSerializer,
    EmailVerificationConfirmSerializer,
    ChangePasswordSerializer,
    UserProfileSerializer,
    UserProfileUpdateSerializer,
)

from .verification import send_verification_email

from .permissions import IsProfileOwner


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "User successfully created."}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
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


class EmailVerificationView(generics.GenericAPIView):
    serializer_class = EmailVerifactionSerializer
    queryset = User.objects.all()

    # TODO setup permissions
    # permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = get_user_model().objects.get(email=email)
            if not user.is_verified:
                token = default_token_generator.make_token(user)
                verification_url = request.build_absolute_uri(
                    reverse('verification_confirm')
                ) + f'?email={email}&token={token}'

                send_verification_email(user, verification_url)

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
                return Response({'detail': 'Email verified'})
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

    serializer_class = UserProfileUpdateSerializer

    def get_permissions(self):
        if self.action in ['retrieve', 'update', 'destroy', 'partial_update']:
            permission_classes = [IsProfileOwner]
        elif self.action == 'list':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action == 'list':
            return UserProfileSerializer
        return UserProfileUpdateSerializer
