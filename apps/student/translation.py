from modeltranslation.translator import register, TranslationOptions

from .models import StudentCouncil, StudentLive


@register(StudentLive)
class StudentLiveTranslation(TranslationOptions):
    fields = ('title', 'description',)


@register(StudentCouncil)
class StudentCouncilTranslation(TranslationOptions):
    fields = ('position', 'description',)
