from django.urls import path, include

from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

from .views import RegisterView, LoginView

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login-phone/', LoginView.as_view(), name='token_obtain_pair_phone'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
]
