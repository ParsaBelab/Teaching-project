from django.test import SimpleTestCase
from django.urls import reverse, resolve
from accounts import views


class AccountsURLsTest(SimpleTestCase):

    def test_register_url_resolves(self):
        url = reverse('accounts:register')
        self.assertEqual(resolve(url).func.view_class, views.RegisterView)

    def test_verify_url_resolves(self):
        url = reverse('accounts:verify')
        self.assertEqual(resolve(url).func.view_class, views.VerifyView)

    def test_login_url_resolves(self):
        url = reverse('accounts:login')
        self.assertEqual(resolve(url).func.view_class, views.LoginView)

    def test_logout_url_resolves(self):
        url = reverse('accounts:logout')
        self.assertEqual(resolve(url).func.view_class, views.LogoutView)

    def test_profile_url_resolves(self):
        url = reverse('accounts:profile', kwargs={'id': 1})
        self.assertEqual(resolve(url).func.view_class, views.ProfileView)

    def test_editprofile_url_resolves(self):
        url = reverse('accounts:editprofile')
        self.assertEqual(resolve(url).func.view_class, views.EditProfileView)

    def test_editpassword_url_resolves(self):
        url = reverse('accounts:editpassword')
        self.assertEqual(resolve(url).func.view_class, views.EditPasswordView)

    def test_resetpassword_url_resolves(self):
        url = reverse('accounts:resetpassword')
        self.assertEqual(resolve(url).func.view_class, views.ResetPasswordView)
