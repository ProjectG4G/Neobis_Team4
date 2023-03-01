from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse

from rest_framework import generics, status

from rest_framework.permissions import AllowAny, IsAuthenticated

from rest_framework.response import Response

from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .serializers import RegisterSerializer, LoginSerializer, EmailVerifactionSerializer
from .verification import send_verification_email


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


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