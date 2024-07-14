from django.test import TestCase, Client
from django.urls import reverse
from accounts.models import User
from accounts.models import OTPCode
from django.contrib.messages import get_messages
from accounts.forms import UserForm, VerifyForm, LoginForm, EditProfileForm, EditPasswordForm, ResetPasswordForm
from django.contrib.auth import authenticate


class RegisterViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('accounts:register')
        self.verify_url = reverse('accounts:verify')
        self.login_url = reverse('accounts:login')
        self.home_url = reverse('Home:home')
        self.user = User.objects.create_user(phone_number='09224201664', username='testuser', password='testpassword')
        self.phone_number = '+989224201664'
        self.otp_code = OTPCode.objects.create(otp_code='1234', phone_number=self.phone_number)

    def test_get_register_view(self):
        # Test GET request to register view
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/register.html')
        self.assertIsInstance(response.context['form'], UserForm)

    def test_post_register_view_new_user(self):
        # Test POST request with valid data for a new user
        data = {
            'username': 'newuser',
            'phone_number': self.phone_number,
            'password': 'newpassword',
        }
        response = self.client.post(self.register_url, data)
        self.assertRedirects(response, self.verify_url)
        self.assertIn('user', self.client.session)
        self.assertEqual(self.client.session['user']['phone_number'], self.phone_number)
        self.assertEqual(self.client.session['user']['username'], 'newuser')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)

    def test_post_register_view_existing_user(self):
        # Test POST request with valid data for an existing user
        User.objects.create_user(username='existinguser', password='existingpassword',
                                 phone_number=self.phone_number)
        data = {
            'username': 'existinguser',
            'phone_number': self.phone_number,
            'password': 'existingpassword',
        }
        response = self.client.post(self.register_url, data)
        self.assertRedirects(response, self.login_url)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 0)

    def test_post_register_view_invalid_form(self):
        # Test POST request with invalid data
        data = {
            'username': 'newuser',
            'phone_number': '',  # Invalid phone number
            'password': 'newpassword',
        }
        form = UserForm(data=data)
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/register.html')
        self.assertTrue(form.has_error)
        self.assertFormError(form, 'phone_number', 'This field is required.')


class VerifyViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.verify_url = reverse('accounts:verify')
        self.home_url = reverse('Home:home')
        self.user_data = {
            'phone_number': '+989224201664',
            'username': 'newtestuser',
            'password': 'newpass',
        }
        self.otp_code = OTPCode.objects.create(otp_code='1234', phone_number=self.user_data['phone_number'])
        self.session = self.client.session
        self.session['user'] = {
            'phone_number': self.user_data['phone_number'],
            'username': self.user_data['username'],
        }
        self.session.save()

    def test_get_verify_view(self):
        response = self.client.get(self.verify_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/verify.html')
        self.assertIsInstance(response.context['form'], VerifyForm)

    def test_post_verify_view_valid_data(self):
        data = {
            'code': '1234',
            'password1': 'newpass',
            'password2': 'newpass',
        }
        response = self.client.post(self.verify_url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.home_url)

        user = authenticate(username=self.user_data['phone_number'], password=data['password1'])
        self.assertIsNotNone(user)

    def test_post_verify_view_invalid_data(self):
        data = {
            'code': '1236',
            'password1': 'newpass',
            'password2': 'newpass',
        }
        response = self.client.post(self.verify_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/verify.html')

    def test_post_verify_view_loggedin_user(self):
        user = User.objects.create_user(phone_number=self.user_data['phone_number'],
                                        username=self.user_data['username'], password=self.user_data['password'])
        self.client.force_login(user)
        data = {
            'code': '1234',
            'password1': 'newpass',
            'password2': 'newpass',
        }
        response = self.client.post(self.verify_url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.home_url)


class LoginViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        phone_number = '09224201664'
        self.user = User.objects.create_user(phone_number=phone_number, username='test', password='1234')
        self.login_url = reverse('accounts:login')
        self.register_url = reverse('accounts:register')
        self.profile_url = reverse('accounts:profile', kwargs={'id': self.user.id})
        self.user_data = {
            'phone_number': phone_number,
            'username': 'test',
            'password': '1234',
        }
        self.session = self.client.session
        self.session['user'] = {
            'phone_number': phone_number,
        }
        self.session.save()

    def test_get_login(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')
        self.assertIsInstance(response.context['form'], LoginForm)

    def test_post_login_valid_data(self):
        data = {
            'password': '1234'
        }
        response = self.client.post(self.login_url, data)
        user = authenticate(username=self.user_data['phone_number'], password=self.user_data['password'])
        self.assertIsNotNone(user)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.profile_url)
        self.assertTrue(user.is_authenticated)

    def test_post_login_invalid_data(self):
        data = {
            'password': '1235'
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.register_url)


class LogoutViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.logout_url = reverse('accounts:logout')
        self.home_url = reverse('Home:home')
        self.user_data = {
            'phone_number': '09224201664',
            'username': 'testuser',
            'password': 'testpass123',
        }
        self.user = User.objects.create_user(**self.user_data)

    def test_get_logout_authenticated(self):
        self.client.login(**self.user_data)
        response = self.client.get(self.logout_url)
        self.assertRedirects(response, self.home_url)
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_post_logout_unauthenticated(self):
        response = self.client.get(self.logout_url)
        self.assertRedirects(response, self.home_url)
        self.assertFalse(response.wsgi_request.user.is_authenticated)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'شما هنوز وارد نشده اید')


class ProfileViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_data = {
            'phone_number': '09224201664',
            'username': 'user',
            'password': '1234',
        }
        self.user = User.objects.create_user(**self.user_data)
        self.profile_url = reverse('accounts:profile', kwargs={'id': self.user.id})
        self.register_url = reverse('accounts:register')

    def test_get_profile_authenticated(self):
        self.client.login(phone_number=self.user_data['phone_number'], password=self.user_data['password'])
        response = self.client.get(self.profile_url)
        self.assertTrue(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/profile.html')
        self.assertEqual(response.context['user'], self.user)

    def test_get_profile_unauthenticated(self):
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 302)
        expected_url = f"{self.register_url}?next={self.profile_url}"
        self.assertRedirects(response, expected_url)


class EditProfileTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_data = {
            'phone_number': '09224201664',
            'username': 'user',
            'password': '1234',
        }
        self.user = User.objects.create_user(**self.user_data)
        self.edit_profile_url = reverse('accounts:editprofile')
        self.profile_url = reverse('accounts:profile', kwargs={'id': self.user.id})
        self.register_url = reverse('accounts:register')

    def test_edit_profile_get_authenticated(self):
        self.client.login(phone_number=self.user_data['phone_number'], password=self.user_data['password'])
        response = self.client.get(self.edit_profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/edit-profile.html')

    def test_edit_profile_get_unauthenticated(self):
        response = self.client.get(self.edit_profile_url)
        self.assertEqual(response.status_code, 302)
        expected_url = f"{self.register_url}?next={self.edit_profile_url}"
        self.assertRedirects(response, expected_url)

    def test_edit_profile_post_auth_valid_data(self):
        self.client.login(phone_number=self.user_data['phone_number'], password=self.user_data['password'])
        new_data = {
            'username': 'newuser',
            'password': '4321',
        }
        response = self.client.post(self.edit_profile_url, new_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.profile_url)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, new_data['username'])

    def test_edit_profile_post_auth_invalid_data(self):
        self.client.login(phone_number=self.user_data['phone_number'], password=self.user_data['password'])
        new_data = {
            'username': '',
            'password': '',
        }
        response = self.client.post(self.edit_profile_url, new_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/edit-profile.html')

        self.assertIsInstance(response.context['form'], EditProfileForm)
        self.assertTrue(response.context['form'].errors)

    def test_edit_profile_unahtuenticated(self):
        new_data = {
            'username': '',
            'password': '',
        }
        response = self.client.post(self.edit_profile_url, new_data)
        self.assertEqual(response.status_code, 302)
        expected_url = f"{self.register_url}?next={self.edit_profile_url}"
        self.assertRedirects(response, expected_url)


class EditPasswordTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.edit_password_url = reverse('accounts:editpassword')
        self.reset_password_url = reverse('accounts:resetpassword')
        self.register_url = reverse('accounts:register')
        self.user_data = {
            'phone_number': '09224201664',
            'username': 'user',
            'password': '1234',
        }
        self.user = User.objects.create_user(**self.user_data)

    def test_edit_password_get_authenticated(self):
        self.client.login(phone_number=self.user_data['phone_number'], password=self.user_data['password'])
        response = self.client.get(self.edit_password_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/edit-password.html')

    def test_edit_password_get_unauth(self):
        response = self.client.get(self.edit_password_url)
        self.assertEqual(response.status_code, 302)
        expected_url = f"{self.register_url}?next={self.edit_password_url}"
        self.assertRedirects(response, expected_url)

    def test_edit_password_post_auth_valid_data(self):
        self.client.login(phone_number=self.user_data['phone_number'], password=self.user_data['password'])
        data = {'password': self.user_data['password']}
        response = self.client.post(self.edit_password_url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.reset_password_url)

    def test_edit_password_post_auth_invalid_data(self):
        self.client.login(phone_number=self.user_data['phone_number'], password=self.user_data['password'])
        data = {'password': ''}
        response = self.client.post(self.edit_password_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/edit-password.html')
        self.assertIsInstance(response.context['form'], EditPasswordForm)

    def est_edit_password_post_unauth(self):
        response = self.client.post(self.edit_password_url)
        self.assertEqual(response.status_code, 302)
        expected_url = f"{self.register_url}?next={self.edit_password_url}"
        self.assertRedirects(response, expected_url)


class ResetPasswordTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_data = {
            'phone_number': '09224201664',
            'username': 'user',
            'password': '1234',
        }
        self.user = User.objects.create_user(**self.user_data)
        self.reset_password_url = reverse('accounts:resetpassword')
        self.profile_url = reverse('accounts:profile', kwargs={'id': self.user.id})

    def test_get_reset_password_authenticated(self):
        self.client.login(phone_number=self.user_data['phone_number'], password=self.user_data['password'])
        response = self.client.get(self.reset_password_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/reset-password.html')
        self.assertIsInstance(response.context['form'], ResetPasswordForm)

    def test_post_reset_password_valid_data(self):
        self.client.login(phone_number=self.user_data['phone_number'], password=self.user_data['password'])
        data = {'password1': 'newpassword123', 'password2': 'newpassword123'}
        response = self.client.post(self.reset_password_url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.profile_url)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('newpassword123'))

    def test_post_reset_password_invalid_data(self):
        self.client.login(phone_number=self.user_data['phone_number'], password=self.user_data['password'])
        data = {'password1': 'newpassword123', 'password2': '1234'}
        response = self.client.post(self.reset_password_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/reset-password.html')
        self.assertIsInstance(response.context['form'], ResetPasswordForm)
