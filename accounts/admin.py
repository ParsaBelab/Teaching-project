from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserChangeForm, UserCreationForm
from .models import User, OTPCode


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ('phone_number', 'username', 'is_admin', 'is_active', 'is_premium', 'premium_to')
    list_filter = ('is_admin', 'is_active')

    fieldsets = (
        (None, {'fields': ('phone_number', 'username', 'password', 'job', 'full_name', 'favorites')}),
        ('دسترسی ها', {'fields': ('is_active', 'is_admin', 'last_login', 'is_premium', 'premium_to')}),
    )
    add_fieldsets = (
        (None, {'fields': ('phone_number', 'username', 'password1', 'password2')}),
    )
    search_fields = ('username', 'phone_number')
    filter_horizontal = ()


admin.site.unregister(Group)
admin.site.register(User, UserAdmin)


class OTPCodeAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'otp_code', 'created')


admin.site.register(OTPCode, OTPCodeAdmin)
