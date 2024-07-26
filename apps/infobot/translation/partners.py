from modeltranslation.translator import TranslationOptions, register

from apps.infobot.models import Partner


@register(Partner)
class PartnerTranslationOptions(TranslationOptions):
    fields = ("name", "description")
