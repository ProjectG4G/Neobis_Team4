from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse

from rest_framework import generics, status, filters

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

from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken

from django_filters.rest_framework import DjangoFilterBackend

from .models import User
from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    EmailVerificationSerializer,
    EmailVerificationConfirmSerializer,
    ChangePasswordSerializer,
    UserProfileSerializer,
    UserProfileUpdateSerializer,
    ModeratorSerializer,
    DummySerializer,
)

from .verification import send_verification_email

from .permissions import IsProfileOwnerOrAdmin

from .filters import UserFilter


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
    serializer_class = EmailVerificationSerializer
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
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_class = UserFilter
    search_fields = ('email', 'phone_number', 'first_name', 'last_name',)

    def get_permissions(self):
        if self.action in ['retrieve', 'update', 'destroy', 'partial_update']:
            permission_classes = [IsProfileOwnerOrAdmin]
        else:
            permission_classes = [IsAdminUser]

        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action == 'list':
            return UserProfileSerializer
        if self.action == 'create':
            return ModeratorSerializer
        # if self.action == 'make_moderator':
        #     return DummySerializer
        # if self.action == 'make_mentor':
        #     return DummySerializer
        return UserProfileUpdateSerializer

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
            return Response({
                'detail': 'New Mentor Added',
                'user': user.id,
            })
        else:
            return Response({
                'detail': 'Mentor Deleted',
                'user': user.id,
            })


class UserRegisterStatisticView(APIView):
    def get(self, request, *args, **kwargs):
        data = dict(
            one=User.objects.filter(date_joined__month=1, date_joined__year=2023).count(),
            two=User.objects.filter(date_joined__month=2, date_joined__year=2023).count(),
            three=User.objects.filter(date_joined__month=3, date_joined__year=2023).count(),
            four=User.objects.filter(date_joined__month=4, date_joined__year=2023).count(),
            five=User.objects.filter(date_joined__month=5, date_joined__year=2023).count(),
            six=User.objects.filter(date_joined__month=6, date_joined__year=2023).count(),
            seven=User.objects.filter(date_joined__month=7, date_joined__year=2023).count(),
            eight=User.objects.filter(date_joined__month=8, date_joined__year=2023).count(),
            nine=User.objects.filter(date_joined__month=9, date_joined__year=2023).count(),
            ten=User.objects.filter(date_joined__month=10, date_joined__year=2023).count(),
            eleven=User.objects.filter(date_joined__month=11, date_joined__year=2023).count(),
            twelve=User.objects.filter(date_joined__month=12, date_joined__year=2023).count(),
        )
        print(data)
        return Response(data)


class ModeratorViewSet(ModelViewSet):
    queryset = User.objects.filter(is_staff=True)
    
    serializer_class = ModeratorSerializer

    permission_classes = [IsAdminUser]
