import random
from django.core.mail import send_mail
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from rest_framework import status
from .serializers import RegisterSerializer
from .models import CustomUser, EmailVerification
from rest_framework.response import Response
from .serializers import PasswordResetRequestSerializer, PasswordResetConfirmSerializer
from django.conf import settings


class RegisterView(CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer

class Users(APIView):
    def get(self, request, format=None):
        user = CustomUser.objects.all()
        serializer = RegisterSerializer(user, many=True)
        return Response(serializer.data)

class UserDetailView(RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer

class PasswordResetRequestView(APIView):
    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Reset link sent"}, status=200)


class PasswordResetConfirmView(APIView):
    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Password changed"}, status=200)


class SendCodeVerify(APIView):
    def post(self, request):
        email = request.data.get("email")

        if not email:
            return Response({"message": "No email"}, status=status.HTTP_400_BAD_REQUEST)

        user = CustomUser.objects.get(email=email)
        code = str(random.randint(100000, 999999))

        EmailVerification.objects.create(user=user, code=code)

        send_mail(
            subject="Email verification",
            message=f"Your verification code: {code}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
        )

        return Response({"message": "Verification code sent"}, status=status.HTTP_200_OK)

class VerifyCode(APIView):
    def post(self, request):
        email = request.data.get("email")
        code = request.data.get("code")

        if not email or not code:
            return Response({"message": "No email or code"}, status=status.HTTP_400_BAD_REQUEST)

        user = CustomUser.objects.get(email=email)
        record = EmailVerification.objects.filter(user=user, code=code)

        if not record:
            return Response({"message": "Verification code not found"}, status=status.HTTP_400_BAD_REQUEST)

        record.user.is_active = True
        record.user.save()
        record.delete()

        return Response({"message": "Email verified successfully"}, status=status.HTTP_200_OK)
