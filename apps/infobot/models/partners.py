from django.db import models

from apps.shared.models import AbstractBaseModel


class Partner(AbstractBaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField()
    logo = models.ImageField(upload_to="partners/")

    class Meta:
        verbose_name = "Hamkor"
        verbose_name_plural = "Hamkorlar"

    def __str__(self):
        return self.name
