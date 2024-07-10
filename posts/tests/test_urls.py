from django.test import SimpleTestCase
from django.urls import reverse, resolve
from posts import views


class TestCategoryURLs(SimpleTestCase):

    def test_category_list_url_resolves(self):
        url = reverse('categories:all')
        self.assertEqual(resolve(url).func.view_class, views.CategoryListView)

    def test_category_detail_url_resolves(self):
        url = reverse('categories:detail', kwargs={'cat_id': 1})
        self.assertEqual(resolve(url).func.view_class, views.CategoryDetailView)
