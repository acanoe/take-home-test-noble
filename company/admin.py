from django.contrib import admin

from .models import Company


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    exclude = ("updated_by",)
    list_display = ("name", "industry")
