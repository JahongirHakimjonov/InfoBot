from modeltranslation.translator import TranslationOptions, register


from apps.infobot.models import News


@register(News)
class NewsTranslationOptions(TranslationOptions):
    fields = ("title", "description")
