from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Additional Info", {"fields": ("phone_number", "status")}),
    )

    list_display = ("username", "email", "phone_number", "status")

admin.site.register(CustomUser, CustomUserAdmin)
