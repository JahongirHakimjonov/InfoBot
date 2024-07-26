from django.contrib import admin

from apps.infobot.models import Service
from unfold.admin import ModelAdmin
from modeltranslation.admin import TabbedTranslationAdmin


@admin.register(Service)
class ServiceAdmin(ModelAdmin, TabbedTranslationAdmin):
    list_display = ("id", "name", "description", "created_at", "updated_at")
    search_fields = ("title", "description")
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")
