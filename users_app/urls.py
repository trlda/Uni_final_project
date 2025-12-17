from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterView, MeView, PasswordResetRequestView, PasswordResetConfirmView, SendCodeVerify, VerifyCode

urlpatterns = [
    path("register/", RegisterView.as_view()),
    path("login/", TokenObtainPairView.as_view()),
    path("token/refresh/", TokenRefreshView.as_view()),
    path("me/", MeView.as_view()),
    path("password-reset/", PasswordResetRequestView.as_view()),
    path("password-reset-confirm/", PasswordResetConfirmView.as_view()),
    path("send-code/", SendCodeVerify.as_view()),
    path("verify-code/", VerifyCode.as_view()),
]