from django.urls import path
from rest_framework.routers import SimpleRouter
from .views import UserCreateAPIView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path("login", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("login/refresh", TokenRefreshView.as_view(), name="token_refresh"),
    path("sign-up", UserCreateAPIView.as_view(), name="signup"),
]
