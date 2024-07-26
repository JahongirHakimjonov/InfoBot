from django.contrib import admin

from apps.infobot.models import FAQ
from unfold.admin import ModelAdmin
from modeltranslation.admin import TabbedTranslationAdmin


@admin.register(FAQ)
class FAQAdmin(ModelAdmin, TabbedTranslationAdmin):
    list_display = ("id", "question", "answer", "created_at")
    search_fields = ("question", "answer")
    list_per_page = 20
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")
