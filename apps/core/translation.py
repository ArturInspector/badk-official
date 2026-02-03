from modeltranslation.translator import register, TranslationOptions

from .models import (
    Cooperation,
    Document,
    DocumentFile,
    EduProcess,
    EduProcessFile,
    InternationalCooperation,
)


@register(InternationalCooperation)
class InternationalCooperationTranslation(TranslationOptions):
    fields = ('title', 'description',)


@register(Cooperation)
class CooperationTranslation(TranslationOptions):
    fields = ('title',)


@register(Document)
class DocumentTranslation(TranslationOptions):
    fields = ('title',)


@register(DocumentFile)
class DocumentFileTranslation(TranslationOptions):
    fields = ('title',)


@register(EduProcess)
class EduProcessTranslation(TranslationOptions):
    fields = ('title',)


@register(EduProcessFile)
class EduProcessFileTranslation(TranslationOptions):
    fields = ('title',)
