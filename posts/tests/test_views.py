from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client
from django.urls import reverse

from accounts.models import User
from posts.models import Category, Post
from django.core.paginator import Page


class CategoryListViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('categories:all')
        Category.objects.create(name='Category 1')
        Category.objects.create(name='Category 2')

    def test_category_list_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts/categories.html')
        self.assertIn('categories', response.context)
        self.assertEqual(len(response.context['categories']), 2)


class CategoryDetailViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(phone_number='09224201665', username='premiumuser',
                                             password='1234')
        self.image = SimpleUploadedFile(name='test_image.jpg', content=b'\x00\x01\x02\x03', content_type='image/jpeg')
        self.category = Category.objects.create(name='Category 1')
        self.url = reverse('categories:detail', kwargs={'cat_id': self.category.id})
        post2 = Post.objects.create(title='Post 2', text='Body 2', author=self.user, image=self.image)
        post1 = Post.objects.create(title='Post 1', text='Body 1', author=self.user, image=self.image)
        self.category.posts.add(post1, post2)

    def test_category_detail_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts/category.html')
        self.assertIn('category', response.context)
        self.assertIn('posts', response.context)
        self.assertEqual(response.context['category'], self.category)
        self.assertIsInstance(response.context['posts'], Page)
        self.assertEqual(response.context['posts'].paginator.count, 2)

    def test_category_detail_view_pagination(self):
        # Test pagination
        response = self.client.get(self.url, {'page': 1})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['posts']), 1)
        self.assertTrue(response.context['posts'].has_next())

        response = self.client.get(self.url, {'page': 2})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['posts']), 1)
        self.assertFalse(response.context['posts'].has_next())
