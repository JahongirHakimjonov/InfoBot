from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.shared.models import AbstractBaseModel


class BotUser(AbstractBaseModel):
    USER_ROLE = (
        ("admin", _("Admin")),
        ("moderator", _("Moderator")),
        ("user", _("Foydalanuvchi")),
    )
    LANGUAGE_CODE = (
        ("uz", _("O'zbek tili")),
        ("ru", _("Rus tili")),
        ("en", _("Ingliz tili")),
    )

    telegram_id = models.BigIntegerField(unique=True, verbose_name=_("Telegram ID"))
    username = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_("Foydalanuvchi nomi"),
    )
    first_name = models.CharField(
        max_length=255, null=True, blank=True, verbose_name=_("Ism")
    )
    last_name = models.CharField(
        max_length=255, null=True, blank=True, verbose_name=_("Familiya")
    )
    phone = models.BigIntegerField(
        null=True, blank=True, unique=True, verbose_name=_("Telefon raqam")
    )
    language_code = models.CharField(
        max_length=10,
        choices=LANGUAGE_CODE,
        default="uz",
        verbose_name=_("Til"),
    )
    is_active = models.BooleanField(default=True, verbose_name=_("Faolmi"))
    role = models.CharField(
        max_length=10, choices=USER_ROLE, default="user", verbose_name=_("Rol")
    )

    class Meta:
        db_table = "bot_users"
        verbose_name = _("Bot foaydalanuvchisi")
        verbose_name_plural = _("Bot foydalanuvchilari")

    def __str__(self):
        return str(self.first_name if self.first_name else _("Bot Foydalnuvchisi"))
