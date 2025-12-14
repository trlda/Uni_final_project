from django.urls import path
from .views import RegisterView, Users, UserDetailView, PasswordResetRequestView, PasswordResetConfirmView, SendCodeVerify, VerifyCode
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("user/", Users.as_view(), name="users_list"),
    path("user/<int:pk>/", UserDetailView.as_view(), name="user_detail"),
    path("register/", RegisterView.as_view(), name="register"),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("password-reset/", PasswordResetRequestView.as_view()),
    path("password-reset-confirm/", PasswordResetConfirmView.as_view()),
    path("send-code/", SendCodeVerify.as_view()),
    path("verify-code/", VerifyCode.as_view()),
]