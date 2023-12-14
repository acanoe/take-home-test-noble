from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    fields = ("email", "company", "user_type", "is_superuser", "is_active")
    list_display = ("email", "company", "user_type", "is_superuser", "is_active")
