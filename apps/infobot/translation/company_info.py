from modeltranslation.translator import TranslationOptions, register

from apps.infobot.models import CompanyInfo


@register(CompanyInfo)
class CompanyInfoTranslationOptions(TranslationOptions):
    fields = ("name", "description", "address")
