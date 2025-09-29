from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser

    list_display = (
        "id",
        "username",
        "email",
        "phone_number",
        "city",
        "is_superuser",
        "is_active",
        "is_staff",
        "first_name",
        "last_name",
        "tg_chat_id",
        "avatar",
        "token"
    )
    # Добавляем новые поля в интерфейс администратора
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (("Personal Info"), {"fields": ("first_name", "last_name", "email", "phone_number", "city", "tg_chat_id",
                                        "avatar", "token")}),
        (("Permissions"), {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        (("Important Dates"), {"fields": ("last_login", "date_joined")}),
    )
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
