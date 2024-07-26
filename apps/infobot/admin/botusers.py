from typing import Callable, TypeVar, cast, Protocol

from django.contrib import admin
from django.db.models.query import QuerySet
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _
from unfold.admin import ModelAdmin

from apps.infobot.models import BotUser


# Define a protocol for actions with a description
class ActionWithDescription(Protocol):
    def __call__(
        self,
        modeladmin: admin.ModelAdmin,
        request: HttpRequest,
        queryset: QuerySet,
    ) -> None: ...

    short_description: str


T = TypeVar("T", bound=Callable[..., None])


def describe_action(action: T, description: str) -> ActionWithDescription:
    # Ensure action is treated as having the ActionWithDescription protocol
    casted_action = cast(ActionWithDescription, action)
    casted_action.short_description = description
    return casted_action


@admin.register(BotUser)
class BotUsersAdmin(ModelAdmin):
    list_display = (
        "id",
        "telegram_id",
        "username",
        "first_name",
        "last_name",
        "phone",
        "language_code",
        "is_active",
        "role",
    )
    list_filter = ("role", "language_code", "is_active")
    search_fields = ("first_name", "last_name", "phone", "username")
    date_hierarchy = "created_at"
    list_per_page = 10
    list_max_show_all = 50
    list_editable = ("is_active", "role", "language_code")
    actions = ["make_active", "make_inactive"]

    ActionWithDescription = Callable[[admin.ModelAdmin, HttpRequest, QuerySet], None]

    def make_active(self, request, queryset):
        queryset.update(is_active=True)

    make_active = describe_action(make_active, _("Faol qilish"))  # Apply custom type

    def make_inactive(self, request, queryset):
        queryset.update(is_active=False)

    make_inactive = describe_action(
        make_inactive, _("Nofaol qilish")
    )  # Apply custom type
