from django.db import models

from apps.shared.models import AbstractBaseModel


class Contact(AbstractBaseModel):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    phone = models.CharField(max_length=255)
    phone2 = models.CharField(max_length=255)
    message = models.TextField(blank=True, null=True)
    address = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Aloqa ma'lumoti"
        verbose_name_plural = "Aloqa ma'lumotlari"

    def __str__(self):
        return self.name
