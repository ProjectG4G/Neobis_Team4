from django.http import HttpResponse
from django.views.generic import View
from django.core.signing import loads, BadSignature, SignatureExpired
from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.urls import reverse

from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from rest_framework.permissions import AllowAny, IsAuthenticated

from .serializers import RegisterSerializer, LoginSerializer, RequestEmailVerifactionSerializer
from rest_framework import generics


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
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            }
        )


class RequestEmailVerificationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RequestEmailVerifactionSerializer
    permission_classes = (AllowAny,)


class EmailVerificationView(View):
    def get(self, request, **kwargs):
        token = kwargs.get('token')

        try:
            user_id = loads(token, max_age=settings.EMAIL_VERIFICATION_TIMEOUT)
        except SignatureExpired:
            return HttpResponse('Verification link has expired.')
        except BadSignature:
            return HttpResponse('Verification link is invalid.')
        else:
            user = get_user_model().objects.get(id=user_id)

            if not user.is_verified:
                user.is_verified = True
                user.save()

            return redirect(reverse('token_obtain_pair'))
