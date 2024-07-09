from django.test import TestCase
from django.utils import timezone
from django.contrib.auth import get_user_model
from datetime import timedelta
from posts.models import Post

User = get_user_model()


class UserModelTest(TestCase):
    def setUp(self):
        self.user_data = {
            'phone_number': '09224201664',
            'username': 'user',
            'password': '1234',
        }
        self.user = User.objects.create_user(**self.user_data)
        self.admin_user = User.objects.create_superuser(
            phone_number='09224201665',
            username='admin',
            password='adminpass'
        )

    def test_user_creation(self):
        self.assertEqual(self.user.phone_number, '09224201664')
        self.assertEqual(self.user.username, 'user')
        self.assertTrue(self.user.check_password('1234'))
        self.assertTrue(self.user.is_active)
        self.assertFalse(self.user.is_admin)
        self.assertFalse(self.user.is_premium)

    def test_admin_user_creation(self):
        self.assertEqual(self.admin_user.phone_number, '09224201665')
        self.assertEqual(self.admin_user.username, 'admin')
        self.assertTrue(self.admin_user.check_password('adminpass'))
        self.assertTrue(self.admin_user.is_active)
        self.assertTrue(self.admin_user.is_admin)
        self.assertFalse(self.admin_user.is_premium)

    def test_str_representation(self):
        self.assertEqual(str(self.user), self.user.username)

    def test_is_staff_property(self):
        self.assertFalse(self.user.is_staff)
        self.assertTrue(self.admin_user.is_staff)

    def test_user_permissions(self):
        self.assertTrue(self.user.has_perm('any_perm'))
        self.assertTrue(self.user.has_module_perms('any_app'))

    def test_premium_status(self):
        self.user.premium_to = timezone.now() + timedelta(days=1)
        self.user.is_premium = True
        self.user.save()
        self.assertTrue(self.user.is_premium)

    def test_favorites_relationship(self):
        post = Post.objects.create(title="Test Post", author=self.admin_user, text="This is a test post")
        self.user.favorites.add(post)
        self.assertIn(post, self.user.favorites.all())

    def test_meta_options(self):
        self.assertEqual(self.user._meta.verbose_name, 'کاربر')
        self.assertEqual(self.user._meta.verbose_name_plural, 'کاربران')
