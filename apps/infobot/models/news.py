from django.db import models

from apps.shared.models import AbstractBaseModel


class News(AbstractBaseModel):
    image = models.ImageField(
        upload_to="services/", null=True, blank=True
    )
    title = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        verbose_name = "Yangilik"
        verbose_name_plural = "Yangiliklar"

    def __str__(self):
        return self.title
