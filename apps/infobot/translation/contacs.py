from modeltranslation.translator import TranslationOptions, register

from apps.infobot.models import Contact


@register(Contact)
class ContactTranslationOptions(TranslationOptions):
    fields = ("name", "message", "address")
