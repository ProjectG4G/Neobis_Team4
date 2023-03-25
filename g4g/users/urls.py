from django.urls import path, include

from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenObtainPairView,
    TokenBlacklistView,
)

from rest_framework.routers import SimpleRouter

from .views import (
    RegisterView,
    LoginPhoneView,
    EmailVerificationConfirmView,
    EmailVerificationView,
    ChangePasswordView,
    UserProfileView,
    UserRegisterStatisticView,
    ModeratorViewSet,
    MentorProfileView,
    LoginEmailView,
)

router = SimpleRouter()
router.register('users', UserProfileView, basename='user')
router.register('moderators', ModeratorViewSet, basename='moderator')

urlpatterns = [
    path('login/', LoginEmailView.as_view(), name='login_email'),
    path('login-phone/', LoginPhoneView.as_view(), name='login_phone'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', TokenBlacklistView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register_phone'),
    path('register/', RegisterView.as_view(), name='register_email'),
    path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('verification/', EmailVerificationView.as_view(), name='verification'),
    path('verification/confirm/', EmailVerificationConfirmView.as_view(), name='verification_confirm'),
    path('', include(router.urls)),
    path('stats/new-users/<int:year>', UserRegisterStatisticView.as_view(), name='stats-new-users'),
    path('users/<int:pk>/mentor_profile/', MentorProfileView.as_view(), name='mentor_profile'),
]
