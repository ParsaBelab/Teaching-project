from django.contrib import admin
from . import models
from modeltranslation.admin import TranslationAdmin

admin.site.register(models.Comment)
admin.site.register(models.Category)
admin.site.register(models.Post)

