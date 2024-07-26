from django.db import models

from apps.shared.models import AbstractBaseModel


class FAQ(AbstractBaseModel):
    question = models.TextField()
    answer = models.TextField()

    class Meta:
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"

    def __str__(self):
        return self.question
