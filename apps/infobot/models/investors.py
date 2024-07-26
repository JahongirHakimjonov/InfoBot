from django.db import models

from apps.shared.models import AbstractBaseModel


class Investor(AbstractBaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField()
    logo = models.ImageField(upload_to="investors/", blank=True, null=True)

    class Meta:
        verbose_name = "Investor"
        verbose_name_plural = "Investorlar"

    def __str__(self):
        return self.name
