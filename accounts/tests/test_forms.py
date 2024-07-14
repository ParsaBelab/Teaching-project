from django.test import TestCase
from accounts.forms import UserCreationForm
from accounts.models import User


class UserCreationFormTest(TestCase):

    def setUp(self):
        self.valid_data = {
            'phone_number': '09224201664',
            'username': 'parsam',
            'password1': '1234',
            'password2': '1234',
        }
        self.invalid_data_password_mismatch = {
            'phone_number': '09224201664',
            'username': 'parsam',
            'password1': '1234',
            'password2': '1235',
        }
        self.invalid_data_missing_field = {
            'phone_number': '',
            'username': 'parsam',
            'password1': '1234',
            'password2': '1234',
        }
        self.invalid_data_invalid_phone = {
            'phone_number': '224201664',
            'username': 'parsam',
            'password1': '1234',
            'password2': '1234',
        }

    def test_form_valid_data(self):
        form = UserCreationForm(data=self.valid_data)
        self.assertTrue(form.is_valid())

    def test_form_password_mismatch(self):
        form = UserCreationForm(data=self.invalid_data_password_mismatch)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)
        self.assertEqual(form.errors['password2'], ['passwords does not match'])

    def test_form_missing_field(self):
        form = UserCreationForm(data=self.invalid_data_missing_field)
        self.assertFalse(form.is_valid())
        self.assertIn('phone_number', form.errors)
        self.assertEqual(form.errors['phone_number'], ['This field is required.'])

    def test_form_invalid_phone_number(self):
        form = UserCreationForm(data=self.invalid_data_invalid_phone)
        self.assertFalse(form.is_valid())
        self.assertIn('phone_number', form.errors)
        self.assertTrue(form.errors['phone_number'])
