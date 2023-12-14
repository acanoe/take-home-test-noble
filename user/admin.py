from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    fields = ("email", "company", "is_superuser", "is_active")
    list_display = ("email", "company", "is_superuser", "is_active")
