from django.urls import path, include

from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenObtainPairView,
    TokenBlacklistView,
)

from rest_framework.routers import SimpleRouter

from .views import (
    RegisterView,
    LoginView,
    EmailVerificationConfirmView,
    EmailVerificationView,
    ChangePasswordView,
    UserProfileView
)

router = SimpleRouter()
router.register('users', UserProfileView, basename='user')

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login-phone/', LoginView.as_view(), name='token_obtain_pair_phone'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', TokenBlacklistView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('verification/', EmailVerificationView.as_view(), name='verification'),
    path('verification/confirm/', EmailVerificationConfirmView.as_view(), name='verification_confirm'),
    path('', include(router.urls)),
]
