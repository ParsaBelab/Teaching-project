from django.test import TestCase, Client
from django.urls import reverse

from home.forms import CommentForm
from posts.models import Post, Category, Comment
from accounts.models import User
from django.core.files.uploadedfile import SimpleUploadedFile


class HomeViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('Home:home')

        # Create sample data
        self.category1 = Category.objects.create(name='Category 1')
        self.category2 = Category.objects.create(name='Category 2')
        self.user = User.objects.create_user(phone_number='09224201664', username='parsam', password='1234')
        self.image = SimpleUploadedFile(name='test_image.jpg', content=b'\x00\x01\x02\x03', content_type='image/jpeg')
        for i in range(5):
            post = Post.objects.create(
                title=f'Post {i + 1}',
                image=self.image,
                text=f'This is the content for post {i + 1}.',
                author=self.user
            )
            if i % 2 == 0:
                post.category.set([self.category1])
            else:
                post.category.set([self.category2])

    def test_home_view_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/index.html')

    def test_home_view_context_data(self):
        response = self.client.get(self.url)
        self.assertIn('posts', response.context)
        self.assertIn('categories', response.context)
        self.assertIn('recent_posts', response.context)

        self.assertEqual(len(response.context['posts']), 1)
        self.assertEqual(len(response.context['categories']), 2)
        self.assertEqual(len(response.context['recent_posts']), 3)

    def test_home_view_pagination(self):
        response = self.client.get(self.url)
        self.assertTrue(response.context['posts'].has_next())
        self.assertEqual(response.context['posts'].number, 1)

        response = self.client.get(self.url, {'page': 2})
        self.assertEqual(response.context['posts'].number, 2)


class PostDetailViewTest(TestCase):
    def setUp(self):
        self.client = Client()

        # Create a user and a premium user
        self.user = User.objects.create_user(phone_number='09224201664', username='user', password='1234')
        self.premium_user = User.objects.create_user(phone_number='09224201665', username='premiumuser',
                                                     password='1234')
        self.premium_user.is_premium = True
        self.premium_user.save()

        # Dummy image file
        self.image = SimpleUploadedFile(name='test_image.jpg', content=b'\x00\x01\x02\x03', content_type='image/jpeg')

        # Create categories and a post
        self.category = Category.objects.create(name='Category 1')
        self.post = Post.objects.create(
            title='Test Post',
            text='This is a test post.',
            author=self.user,
            image=self.image,
            slug='test-post'
        )
        self.post.category.set([self.category])
        self.post_detail_url = reverse('Home:post-detail', kwargs={'post_id': self.post.id, 'slug': self.post.slug})

    def test_redirect_if_not_authenticated(self):
        response = self.client.get(self.post_detail_url)
        self.assertRedirects(response, reverse('accounts:register'))

    def test_redirect_if_not_premium(self):
        self.client.login(phone_number=self.user.phone_number, password='1234')
        response = self.client.get(self.post_detail_url)
        self.assertRedirects(response, reverse('Home:home'))

    def test_get_post_detail_authenticated_and_premium(self):
        self.client.login(phone_number=self.premium_user.phone_number, password='1234')
        response = self.client.get(self.post_detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/post-detail.html')
        self.assertEqual(response.context['post'], self.post)
        self.assertIsInstance(response.context['form'], CommentForm)

    def test_post_comment_authenticated_and_premium(self):
        self.client.login(phone_number=self.premium_user.phone_number, password='1234')
        self.comment = Comment.objects.create(author=self.user, post=self.post, body='test comment')
        response = self.client.post(self.post_detail_url)
        self.assertRedirects(response, self.post_detail_url)
        comments = Comment.objects.filter(post=self.post)
        self.assertEqual(comments.count(), 1)
        self.assertEqual(comments.first().author, self.user)


class AddReplyViewTest(TestCase):
    def setUp(self):
        self.client = Client()

        self.user = User.objects.create_user(phone_number='09224201665', username='premiumuser',
                                             password='1234')

        # Dummy image file
        self.image = SimpleUploadedFile(name='test_image.jpg', content=b'\x00\x01\x02\x03', content_type='image/jpeg')

        # Create categories, a post, and a comment
        self.category = Category.objects.create(name='Category 1')
        self.post = Post.objects.create(
            title='Test Post',
            text='This is a test post.',
            author=self.user,
            image=self.image,
            slug='test-post'
        )
        self.post.category.set([self.category])

        self.comment = Comment.objects.create(
            post=self.post,
            author=self.user,
            body='This is a test comment.',
        )

        self.reply_url = reverse('Home:reply', kwargs={'slug': self.post.slug, 'post_id': self.post.id,
                                                       'comment_id': self.comment.id})
        self.post_detail_url = reverse('Home:post-detail', kwargs={'post_id': self.post.id, 'slug': self.post.slug})

        # Create form data for reply
        # self.reply = Comment.objects.create(
        #     post=self.post,
        #     author=self.user,
        #     body='This is a test comment.',
        #     parent= self.comment
        # )
        self.reply_data = {'body': 'hello'}

    def test_redirect_if_not_authenticated(self):
        response = self.client.get(self.reply_url)
        self.assertRedirects(response, reverse('accounts:register'))

    def test_post_reply_authenticated(self):
        self.client.login(phone_number=self.user.phone_number, password='1234')
        response = self.client.post(self.reply_url, self.reply_data)
        self.assertEqual(response.status_code, 302)
        replies = Comment.objects.filter(parent=self.comment)
        self.assertEqual(replies.count(), 1)
        self.assertEqual(replies.first().author, self.user)
        self.assertTrue(replies.first().is_reply)

    def test_invalid_reply_data(self):
        self.client.login(phone_number=self.user.phone_number, password='1234')
        response = self.client.post(self.reply_url, {})
        self.assertEqual(response.status_code, 302)
        replies = Comment.objects.filter(parent=self.comment)
        self.assertEqual(replies.count(), 0)

    def test_post_reply_to_nonexistent_comment(self):
        self.client.login(phone_number=self.user.phone_number, password='1234')
        invalid_reply_url = reverse('Home:reply',
                                    kwargs={'slug': self.post.slug, 'post_id': self.post.id, 'comment_id': 999})
        response = self.client.post(invalid_reply_url, self.reply_data)
        self.assertEqual(response.status_code, 404)
