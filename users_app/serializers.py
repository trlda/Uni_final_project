from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.conf import settings
from .models import CustomUser

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ("id", "username", "email", "phone_number", "password", "password2")
        read_only_fields = ("id",)

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"password": "Passwords do not match"})
        return attrs

    def create(self, validated_data):
        validated_data.pop("password2")

        user = CustomUser.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            phone_number=validated_data.get("phone_number"),
            password=validated_data["password"],
        )

        user.is_active = False
        user.save()
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("id", "username", "email", "phone_number", "status")


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def save(self):
        user = CustomUser.objects.filter(email=self.validated_data["email"]).first()
        if not user:
            raise serializers.ValidationError({"email": "User not found"})

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        link = f"{settings.FRONTEND_URL}/reset_password.html?uid={uid}&token={token}"

        send_mail(
            subject="Password reset",
            message=f"Reset password:\n{link}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
        )


class PasswordResetConfirmSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(validators=[validate_password])

    def save(self):
        uid = urlsafe_base64_decode(self.validated_data["uid"]).decode()
        user = CustomUser.objects.get(pk=uid)

        if not default_token_generator.check_token(user, self.validated_data["token"]):
            raise serializers.ValidationError("Invalid token")

        user.set_password(self.validated_data["new_password"])
        user.save()
