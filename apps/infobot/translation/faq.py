from modeltranslation.translator import TranslationOptions, register


from apps.infobot.models import FAQ


@register(FAQ)
class FAQTranslationOptions(TranslationOptions):
    fields = ("question", "answer")
