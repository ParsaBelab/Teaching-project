from django.db import models
from django.utils import translation
from persiantools.jdatetime import JalaliDateTime
from datetime import datetime


class ConvertDatesMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if translation.get_language() == 'fa':
            self.convert_dates(request)
        return response

    def convert_dates(self, request):
        if hasattr(request, 'jalali_date_conversion'):
            return  # Prevent multiple conversions in one request

        request.jalali_date_conversion = True

        for model in self.get_all_models():
            for instance in model.objects.all():
                self.convert_instance_dates(instance)

    def get_all_models(self):
        from django.apps import apps
        models = []
        for model in apps.get_models():
            if hasattr(model, 'convert_to_jalali'):
                models.append(model)
        return models

    def convert_instance_dates(self, instance):
        for field in instance._meta.get_fields():
            if isinstance(field, (models.DateField, models.DateTimeField)):
                date_value = getattr(instance, field.name)
                if date_value and isinstance(date_value, datetime):
                    jalali_date = JalaliDateTime.to_jalali(date_value)
                    setattr(instance, field.name, jalali_date)
