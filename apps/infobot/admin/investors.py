from django.contrib import admin

from apps.infobot.models import Investor
from unfold.admin import ModelAdmin
from modeltranslation.admin import TabbedTranslationAdmin


@admin.register(Investor)
class InvestorAdmin(ModelAdmin, TabbedTranslationAdmin):
    list_display = ("id", "name", "created_at", "description")
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")
