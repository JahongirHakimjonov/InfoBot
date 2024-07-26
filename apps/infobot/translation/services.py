from modeltranslation.translator import TranslationOptions, register

from apps.infobot.models import Service


@register(Service)
class ServiceTranslationOptions(TranslationOptions):
    fields = ("name", "description")
