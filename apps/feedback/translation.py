from modeltranslation.translator import register, TranslationOptions

from .models import FeedBack


@register(FeedBack)
class FeedBackTranslation(TranslationOptions):
    fields = ('name', 'message',)


