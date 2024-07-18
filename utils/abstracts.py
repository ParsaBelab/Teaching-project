from django.db import models
from .mixins import MiladiToJalaliMixin


class AbstractDateTime(MiladiToJalaliMixin, models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
