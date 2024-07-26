from django.db import models

from apps.shared.models import AbstractBaseModel


class Service(AbstractBaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField()
    logo = models.ImageField(
        upload_to="services/", null=True, blank=True
    )

    class Meta:
        verbose_name = "Xizmat"
        verbose_name_plural = "Xizmatlar"

    def __str__(self):
        return self.name
