from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin
from unfold.admin import ModelAdmin

from apps.infobot.models import Partner


@admin.register(Partner)
class PartnerAdmin(ModelAdmin, TabbedTranslationAdmin):
    list_display = ("id", "name", "description", "created_at")
    required_languages: tuple = ("uz",)
    search_fields = ("name", "description")
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")
