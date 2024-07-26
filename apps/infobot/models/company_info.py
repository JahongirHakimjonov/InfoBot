from django.db import models

from apps.shared.models import AbstractBaseModel


class CompanyInfo(AbstractBaseModel):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)
    email = models.EmailField()
    website = models.URLField()
    description = models.TextField()

    class Meta:
        verbose_name = "Kompaniya ma'lumoti"
        verbose_name_plural = "Kompaniya ma'lumotlari"

    def __str__(self):
        return self.name
