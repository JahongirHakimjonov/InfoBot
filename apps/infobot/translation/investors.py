from modeltranslation.translator import TranslationOptions, register

from apps.infobot.models import Investor


@register(Investor)
class InvestorTranslationOptions(TranslationOptions):
    fields = ("name", "description")
