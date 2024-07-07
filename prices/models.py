from django.db import models


class Price(models.Model):
    name = models.CharField(max_length=50, verbose_name='عنوان')
    days = models.PositiveSmallIntegerField(verbose_name='روز های اشتراک')
    value = models.PositiveIntegerField(verbose_name='قیمت')

    class Meta:
        ordering = ('days',)

    def __str__(self):
        return self.name
