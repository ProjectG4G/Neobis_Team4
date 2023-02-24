from django.urls import path

from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenObtainPairView,
    TokenBlacklistView,
)

from .views import RegisterView, LoginView, EmailVerificationConfirmView, EmailVerificationView

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login-phone/', LoginView.as_view(), name='token_obtain_pair_phone'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', TokenBlacklistView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('verification/', EmailVerificationView.as_view(), name='verification'),
    path('verification/confirm/', EmailVerificationConfirmView.as_view(), name='email-verification')
]
