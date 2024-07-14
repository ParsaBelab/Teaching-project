from modeltranslation.translator import translator, TranslationOptions
from .models import Price


class PriceTranslationOptions(TranslationOptions):
    fields = ('name', 'value')


translator.register(Price, PriceTranslationOptions)
