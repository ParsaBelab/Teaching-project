from django.test import TestCase
from django.urls import reverse, resolve
from home import views
from home.views import ToggleFavoriteView

class HomeURLsTest(TestCase):
    def test_home_url(self):
        url = reverse('Home:home')
        self.assertEqual(resolve(url).func.view_class, views.HomeView)

    def test_post_detail_url(self):
        url = reverse('Home:post-detail', kwargs={'post_id': 1, 'slug': 'test-post'})
        self.assertEqual(resolve(url).func.view_class, views.PostDetailView)

    def test_add_reply_url(self):
        url = reverse('Home:reply', kwargs={'slug': 'test-post', 'post_id': 1, 'comment_id': 1})
        self.assertEqual(resolve(url).func.view_class, views.AddReplyView)

    def test_toggle_favorite_url(self):
        url = reverse('Home:toggle_favorite', kwargs={'post_id': 1})
        self.assertEqual(resolve(url).func.view_class, ToggleFavoriteView)
