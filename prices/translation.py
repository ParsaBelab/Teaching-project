from modeltranslation.translator import translator, TranslationOptions
from .models import Post


class PostTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'text')


translator.register(Post, PostTranslationOptions)
