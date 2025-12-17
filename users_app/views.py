import random
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import CustomUser, EmailVerification
from .serializers import RegisterSerializer, UserSerializer, PasswordResetRequestSerializer, PasswordResetConfirmSerializer

class RegisterView(CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer

class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class PasswordResetRequestView(APIView):
    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Reset link sent"})


class PasswordResetConfirmView(APIView):
    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Password changed"})


class SendCodeVerify(APIView):
    def post(self, request):
        email = request.data.get("email")
        user = CustomUser.objects.filter(email=email).first()

        if not user:
            return Response({"message": "User not found"}, status=404)

        EmailVerification.objects.filter(user=user).delete()

        code = str(random.randint(100000, 999999))
        EmailVerification.objects.create(user=user, code=code)

        send_mail(
            "Email verification",
            f"Your code: {code}",
            settings.EMAIL_HOST_USER,
            [email],
        )

        return Response({"message": "Code sent"})


class VerifyCode(APIView):
    def post(self, request):
        email = request.data.get("email")
        code = request.data.get("code")

        user = CustomUser.objects.filter(email=email).first()
        record = EmailVerification.objects.filter(user=user, code=code).first()

        if not record:
            return Response({"message": "Invalid code"}, status=400)

        user.is_active = True
        user.save()
        record.delete()

        return Response({"message": "Email verified"})
