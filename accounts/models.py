# django apps
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .managers import UserManager
from django.utils.translation import gettext_lazy as _

# third-party apps
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractBaseUser):
    phone_number = PhoneNumberField(
        unique=True,
        max_length=13,
        verbose_name=_('phone number')
    )
    username = models.CharField(
        max_length=60,
        verbose_name=_('username')
    )
    is_active = models.BooleanField(
        default=False,
        verbose_name=_('active')
    )
    is_admin = models.BooleanField(
        default=False, verbose_name=_('admin')
    )
    is_premium = models.BooleanField(
        default=False,
        verbose_name=_('premium')
    )
    premium_to = models.DateTimeField(
        verbose_name=_('premium to'),
        blank=True,
        null=True
    )
    job = models.CharField(
        max_length=80,
        null=True,
        blank=True,
        verbose_name=_('job')
    )
    full_name = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name=_('full name')
    )
    favorites = models.ManyToManyField(
        'posts.Post',
        related_name='favorite_by',
        blank=True,
        verbose_name='favorites'
    )

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['username']
    objects = UserManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')


class OTPCode(models.Model):
    phone_number = PhoneNumberField(verbose_name=_('phone number'))
    otp_code = models.PositiveSmallIntegerField(verbose_name=_('code'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('created'))

    def __str__(self):
        return f'{self.phone_number} - {self.otp_code} - {self.created}'
