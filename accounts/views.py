from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from random import randint
from accounts.forms import *
from accounts.models import User, OTPCode
from django.contrib import messages


class RegisterView(View):
    form_class = UserForm
    template_name = 'accounts/register.html'

    def dispatch(self, request, *args, **kwargs):
        print(request.user)
        if request.user.is_authenticated:
            messages.error(request, 'شما قبلا وارد شده اید', 'danger')
            return redirect('Home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']
            user = User.objects.filter(phone_number=phone_number).exists()
            request.session['user'] = {
                'phone_number': str(phone_number),
                'username': form.cleaned_data['username'],
            }
            if not user:
                code = OTPCode.objects.filter(phone_number=phone_number).exists()
                if not code:
                    otp_code = randint(1000, 9999)
                    OTPCode.objects.create(otp_code=otp_code, phone_number=phone_number)
                    messages.error(request, 'کد تایید برای شما ارسال شد', 'success')
                    return redirect('accounts:verify')
                messages.error(request, 'برای این شماره قبلا کد ارسال شده', 'error')
                return redirect('accounts:verify')
            return redirect('accounts:login')
        return render(request, self.template_name, {'form': self.form_class})


class VerifyView(View):
    form_class = VerifyForm
    template_name = 'accounts/verify.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.error(request, 'شما قبلا وارد شده اید', 'danger')
            return redirect('Home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            phone_number = request.session['user']['phone_number']
            username = request.session['user']['username']
            otp_code = OTPCode.objects.get(phone_number=phone_number).otp_code
            if otp_code == cd['code']:
                User.objects.create_user(phone_number=phone_number, username=username,
                                         password=cd['password1'])

                user = authenticate(request, username=phone_number, password=cd['password1'])
                if user is not None:
                    login(request, user)
                return redirect('Home:home')
            else:
                messages.error(request, 'کد اشتباه است', 'error')
        return render(request, self.template_name, {'form': form})


class LoginView(View):
    form_class = LoginForm
    template_name = 'accounts/login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.error(request, 'شما قبلا وارد شده اید', 'danger')
            return redirect('Home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            phone_number = request.session['user']['phone_number']
            user = authenticate(request, username=phone_number, password=cd['password'])
            if user is not None:
                login(request, user)
            return redirect('Home:home')


class LogoutView(View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'شما هنوز وارد نشده اید', 'danger')
            return redirect('Home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        logout(request)
        return redirect('Home:home')


class ProfileView(LoginRequiredMixin, View):
    template_name = 'accounts/profile.html'

    def get(self, request, id):
        user = get_object_or_404(User, id=id)

        return render(request, self.template_name, {'user': user})


class EditProfileView(LoginRequiredMixin, View):
    form_class = EditProfileForm
    template_name = 'accounts/edit-profile.html'

    def get(self, request):
        form = self.form_class(instance=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('accounts:profile', request.user.id)
        return render(request, self.template_name, {'form': form})


class EditPasswordView(LoginRequiredMixin, View):
    form_class = EditPasswordForm
    template_name = 'accounts/edit-password.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            if request.user.check_password(password):
                return redirect('accounts:resetpassword')
        return render(request, self.template_name, {'form': form})


class ResetPasswordView(LoginRequiredMixin, View):
    form_class = ResetPasswordForm
    template_name = 'accounts/reset-password.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password1']
            user = request.user
            phone_number = user.phone_number
            user.set_password(password)
            user.save()
            edited_user = authenticate(request, username=phone_number, password=password)
            if edited_user:
                login(request, edited_user)
            return redirect('accounts:profile', request.user.id)
        return render(request, self.template_name, {'form': form})
