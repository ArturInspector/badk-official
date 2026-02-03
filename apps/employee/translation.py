from modeltranslation.translator import register, TranslationOptions

from .models import Employee, Nationality, Position


@register(Position)
class PositionTranslation(TranslationOptions):
    fields = ('title', 'short_title',)


@register(Nationality)
class NationalityTranslation(TranslationOptions):
    fields = ('title',)


@register(Employee)
class EmployeeTranslation(TranslationOptions):
    fields = ('description', 'work_skills',)

