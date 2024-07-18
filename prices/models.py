from django.db import models
from django.utils.translation import gettext_lazy as _

from utils.abstracts import AbstractDateTime
from utils.mixins import MiladiToJalaliMixin


class Price(AbstractDateTime, MiladiToJalaliMixin, models.Model):
    name = models.CharField(
        _('title'),
        max_length=50
    )
    days = models.PositiveSmallIntegerField(
        _('days')
    )
    value = models.PositiveIntegerField(
        _('value'),
    )

    class Meta:
        ordering = ('days',)
        verbose_name = _('Plan')
        verbose_name_plural = _('Plans')

    def __str__(self):
        return self.name
