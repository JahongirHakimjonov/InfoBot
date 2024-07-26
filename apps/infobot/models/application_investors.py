from django.db import models

from apps.infobot.choices import StatusChoices
from apps.shared.models import AbstractBaseModel


class ApplicationInvestor(AbstractBaseModel):
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    message = models.TextField(blank=True, null=True)
    status = models.CharField(
        choices=StatusChoices.choices, default=StatusChoices.PENDING, max_length=30
    )

    def __str__(self):
        return self.full_name if self.full_name else self.phone

    class Meta:
        verbose_name = "Investorlik arizasi"
        verbose_name_plural = "Investorlik arizalari"