from django.contrib import admin
from django.contrib.auth.models import Group
from unfold.admin import ModelAdmin

# admin.site.unregister(User)
admin.site.unregister(Group)


# @admin.register(User)
# class CustomUserAdmin(ModelAdmin):
#     list_display = ["id", "username", "email", "is_staff", "is_active", "date_joined"]


@admin.register(Group)
class CustomGroupAdmin(ModelAdmin):
    list_display = ["id", "name"]
