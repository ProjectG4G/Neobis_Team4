from django.urls import path, include

from rest_framework_simplejwt.views import (
    TokenRefreshView,
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
    UserProfileRetrieveView,
    ResetPasswordConfirmView,
    ResetPasswordView,
    ResetPasswordValidateView,
)

router = SimpleRouter()
router.register("users", UserProfileView, basename="user")
router.register("moderators", ModeratorViewSet, basename="moderator")

urlpatterns = [
    path("login/", LoginEmailView.as_view(), name="login_email"),
    path("login_phone/", LoginPhoneView.as_view(), name="login_phone"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("logout/", TokenBlacklistView.as_view(), name="logout"),
    path("register/", RegisterView.as_view(), name="register_email"),
    path("password_reset/", ResetPasswordView.as_view(), name="password_reset"),
    path(
        "password_reset/validate_token/",
        ResetPasswordConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "password_reset/validate",
        ResetPasswordValidateView.as_view(),
        name="password_reset_validate",
    ),
    path("password_change/", ChangePasswordView.as_view(), name="password_change"),
    path("verification/", EmailVerificationView.as_view(), name="verification"),
    path(
        "verification/confirm/",
        EmailVerificationConfirmView.as_view(),
        name="verification_confirm",
    ),
    path(
        "users/<int:pk>/mentor_profile/",
        MentorProfileView.as_view(),
        name="mentor_profile",
    ),
    path("user_profile/", UserProfileRetrieveView.as_view(), name="user_profile"),
    path(
        "stats/new-users/<int:year>",
        UserRegisterStatisticView.as_view(),
        name="stats-new-users",
    ),
    path("", include(router.urls)),
]
