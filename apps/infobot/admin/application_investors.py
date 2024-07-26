from django.contrib import admin

from apps.infobot.models import ApplicationInvestor
from unfold.admin import ModelAdmin


@admin.register(ApplicationInvestor)
class ApplicationInvestorAdmin(ModelAdmin):
    list_display = ("id", "full_name", "phone", "status", "created_at")
    list_filter = ("status", "created_at", "updated_at")
    search_fields = ("full_name", "phone")
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")
