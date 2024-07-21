from django.db import models
from persiantools.jdatetime import JalaliDate


class AbstractDateTime(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
    @property
    def get_created_persian(self):
        jcreated = JalaliDate(self.created,locale='fa')
        return jcreated.strftime('%c',locale='fa')
    @property
    def get_updated_persian(self):
        jupdated = JalaliDate(self.updated,locale='fa')
        return jupdated
