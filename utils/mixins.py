from persiantools.jdatetime import JalaliDateTime
from datetime import datetime
from django.utils import translation
from django.contrib import admin


class MiladiToJalaliMixin:

    def get_jalali_date(self, date_field):
        date_value = getattr(self, date_field)
        if translation.get_language() == 'fa' and date_value:
            return JalaliDateTime.to_jalali(date_value)
        return date_value

    @property
    def jalali_created(self):
        return self.get_jalali_date('created')

    @property
    def jalali_updated(self):
        return self.get_jalali_date('updated')


class AdminTimeMixin(admin.ModelAdmin):
    readonly_fields = ('created', 'updated')
    list_filter = ('created', 'updated')
