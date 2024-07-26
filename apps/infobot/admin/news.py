from django.contrib import admin

from apps.infobot.models import News
from unfold.admin import ModelAdmin
from modeltranslation.admin import TabbedTranslationAdmin


@admin.register(News)
class NewsAdmin(ModelAdmin, TabbedTranslationAdmin):
    list_display = ("id", "title", "description", "created_at", "updated_at")
    search_fields = ("title", "description")
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")
