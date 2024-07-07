from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

from .models import User
from phonenumber_field.formfields import PhoneNumberField


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='رمز عبور', widget=forms.PasswordInput)
    password2 = forms.CharField(label='تایید رمز عبور', widget=forms.PasswordInput)
    phone_number = PhoneNumberField(region='IR')

    class Meta:
        model = User
        fields = ('phone_number', 'username')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] and cd['password2'] and cd['password1'] != cd['password2']:
            raise ValidationError('رمز عبور یکسان نیست')
        return cd['password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(
        help_text='شما میتوانید رمز عبور خود را از<a href="../password">این لینک </a>عوض کنید')

    class Meta:
        model = User
        fields = '__all__'


class UserForm(forms.Form):
    phone_number = PhoneNumberField(region='IR', label='شماره تلفن')
    username = forms.CharField(label='نام کاربری')


class VerifyForm(forms.Form):
    code = forms.IntegerField(label='کد', widget=forms.PasswordInput)
    password1 = forms.CharField(label='رمز عبور', widget=forms.PasswordInput)
    password2 = forms.CharField(label='تایید رمز عبور', widget=forms.PasswordInput)

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] and cd['password2'] and cd['password1'] != cd['password2']:
            raise ValidationError('رمز عبور یکسان نیست')
        return cd['password2']


class LoginForm(forms.Form):
    password = forms.CharField(label='رمز عبور', widget=forms.PasswordInput)


class EditProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = User
        fields = ('username', 'full_name', 'job')


class EditPasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                               label='پسورد فعلی خود را وارد کنید')


class ResetPasswordForm(forms.Form):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                                label='پسورد جدید')
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                                label='تایید پسورد')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] and cd['password2'] and cd['password1'] != cd['password2']:
            raise ValidationError('رمز عبور یکسان نیست')
        return cd['password2']
