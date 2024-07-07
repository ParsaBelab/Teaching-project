from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .managers import UserManager
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractBaseUser):
    phone_number = PhoneNumberField(unique=True, max_length=13, verbose_name='شماره تلفن')
    username = models.CharField(max_length=60, verbose_name='نام کاربری')
    is_active = models.BooleanField(default=False, verbose_name='کاربر فعال')
    is_admin = models.BooleanField(default=False, verbose_name='ادمین')
    is_premium = models.BooleanField(default=False, verbose_name='ویژه')
    premium_to = models.DateTimeField(verbose_name='ویژه تا', blank=True, null=True)
    job = models.CharField(max_length=80, null=True, blank=True, verbose_name='شغل')
    full_name = models.CharField(max_length=100, null=True, blank=True, verbose_name='نام کامل')
    created = models.DateTimeField(auto_now_add=True, verbose_name='ایچاد شده')
    updated = models.DateTimeField(auto_now=True, verbose_name='آپدیت شده')
    favorites = models.ManyToManyField('posts.Post', related_name='favorited_by', blank=True)

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
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'


class OTPCode(models.Model):
    phone_number = PhoneNumberField()
    otp_code = models.PositiveSmallIntegerField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.phone_number} - {self.otp_code} - {self.created}'
