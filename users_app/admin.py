from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Additional Info", {"fields": ("phone_number", "is_vip")}),
    )

    list_display = ("username", "email", "phone_number", "is_vip", "is_default")
    list_filter = ("is_vip", "is_default")
