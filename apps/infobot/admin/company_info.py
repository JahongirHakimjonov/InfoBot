from django.contrib import admin
from unfold.admin import ModelAdmin
from apps.infobot.models import CompanyInfo
from modeltranslation.admin import TabbedTranslationAdmin


@admin.register(CompanyInfo)
class CompanyInfoAdmin(ModelAdmin, TabbedTranslationAdmin):
    list_display = ("id", "name", "address", "created_at", "phone")
    search_fields = ("name", "phone")
    list_per_page = 20
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")
