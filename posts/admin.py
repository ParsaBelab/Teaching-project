from django.contrib import admin
from . import models
from utils.mixins import AdminTimeMixin

admin.site.register(models.Comment)
admin.site.register(models.Category)


@admin.register(models.Post)
class PostAdmin(AdminTimeMixin):
    readonly_fields = ('slug', *AdminTimeMixin.readonly_fields)
