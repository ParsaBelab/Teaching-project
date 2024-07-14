from django.db import models
from django.utils.translation import gettext_lazy as _


class Price(models.Model):
    name = models.CharField(_('name'), max_length=50)
    days = models.PositiveSmallIntegerField(_('days'))
    value = models.PositiveIntegerField(_('value'), )

    class Meta:
        ordering = ('days',)
        verbose_name = _('Price')
        verbose_name_plural = _('Prices')

    def __str__(self):
        return self.name
