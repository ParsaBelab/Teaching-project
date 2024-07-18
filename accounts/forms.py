from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import User
# third-party
from phonenumber_field.formfields import PhoneNumberField


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label=_('password'), widget=forms.PasswordInput)
    password2 = forms.CharField(label=_('submit password'), widget=forms.PasswordInput)
    phone_number = PhoneNumberField(region='IR')

    class Meta:
        model = User
        fields = ('phone_number', 'username')
        labels = {
            'phone_number': _('phone number'),
            'username': _('username'),
        }

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] and cd['password2'] and cd['password1'] != cd['password2']:
            raise ValidationError(_('passwords does not match'))
        return cd['password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(
        help_text=_('you can change your password from <a href="../password"> link'))

    # 'شما میتوانید رمز عبور خود را از<a href="../password">این لینک </a>عوض کنید'

    class Meta:
        model = User
        fields = '__all__'


class UserForm(forms.Form):
    phone_number = PhoneNumberField(region='IR', label=_('phone number'))
    username = forms.CharField(label=_('username'))


class VerifyForm(forms.Form):
    code = forms.IntegerField(label=_('code'), widget=forms.PasswordInput)
    password1 = forms.CharField(label=_('password'), widget=forms.PasswordInput)
    password2 = forms.CharField(label=_('submit password'), widget=forms.PasswordInput)

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] and cd['password2'] and cd['password1'] != cd['password2']:
            raise ValidationError(_('passwords does not match'))
        return cd['password2']


class LoginForm(forms.Form):
    password = forms.CharField(label=_('password'), widget=forms.PasswordInput)


class EditProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = User
        fields = ('username', 'full_name', 'job')
        labels = {'username': _('Username'), 'full_name': _('full_name'), 'job': _('Job')}


class EditPasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                               label=_('Enter current password'))


class ResetPasswordForm(forms.Form):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                                label=_('new password'))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                                label=_('submit new password'))

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] and cd['password2'] and cd['password1'] != cd['password2']:
            raise ValidationError(_('passwords does not match'))
        return cd['password2']
