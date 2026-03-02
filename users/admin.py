from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model

User = get_user_model()


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ("username", "email", "currency_preference", "is_staff")
    list_filter = ("is_staff", "is_superuser", "is_active")
    search_fields = ("username", "email")
    ordering = ("username",)

    fieldsets = UserAdmin.fieldsets + (
        ("Additional Info", {
            "fields": ("currency_preference", "timezone"),
        }),
    )