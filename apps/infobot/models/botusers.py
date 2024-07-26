from django.db import models

from apps.shared.models import AbstractBaseModel


class BotUser(AbstractBaseModel):
    USER_ROLE = (
        ("admin", "Admin"),
        ("moderator", "Moderator"),
        ("user", "Foydalanuvchi"),
    )
    LANGUAGE_CODE = (
        ("uz", "O'zbek tili"),
        ("ru", "Rus tili"),
        ("en", "Ingliz tili"),
    )

    telegram_id = models.BigIntegerField(unique=True)
    username = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    first_name = models.CharField(
        max_length=255, null=True, blank=True
    )
    last_name = models.CharField(
        max_length=255, null=True, blank=True
    )
    phone = models.BigIntegerField(
        null=True, blank=True, unique=True
    )
    language_code = models.CharField(
        max_length=10,
        choices=LANGUAGE_CODE,
        default="uz",
    )
    is_active = models.BooleanField(default=True)
    role = models.CharField(
        max_length=10, choices=USER_ROLE, default="user"
    )

    class Meta:
        db_table = "bot_users"
        verbose_name = "Bot foaydalanuvchisi"
        verbose_name_plural = "Bot foydalanuvchilari"

    def __str__(self):
        return str(self.first_name if self.first_name else "Bot Foydalnuvchisi")
