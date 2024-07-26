from django.contrib import admin
from unfold.admin import ModelAdmin
from apps.infobot.models import ApplicationPartner


@admin.register(ApplicationPartner)
class ApplicationPartnerAdmin(ModelAdmin):
    list_display = ("id", "full_name", "phone", "address", "created_at", "status")
    list_filter = ("status",)
    search_fields = ("full_name", "phone")
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")
