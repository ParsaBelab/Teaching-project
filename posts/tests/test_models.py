from django.test import TestCase
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from posts.models import Post, Category, Comment
from django.urls import reverse

User = get_user_model()


class PostModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(phone_number='09224201664', username='testuser', password='1234')
        self.category1 = Category.objects.create(name='Category 1')
        self.category2 = Category.objects.create(name='Category 2')
        self.post = Post.objects.create(
            title='Test Post',
            image='posts/image/test_image.jpg',
            author=self.user,
            post_type='NORMAL',
            description='Test Description',
            text='Test Text'
        )
        self.post.category.set([self.category1.pk, self.category2.pk])

    def test_create_post(self):
        post = Post.objects.create(
            title='Another Test Post',
            image='posts/image/another_test_image.jpg',
            author=self.user,
            post_type='VIP',
            description='Another Test Description',
            text='Another Test Text'
        )
        post.category.set([self.category1.pk])
        self.assertEqual(post.title, 'Another Test Post')
        self.assertEqual(post.image, 'posts/image/another_test_image.jpg')
        self.assertEqual(post.author, self.user)
        self.assertEqual(post.post_type, 'VIP')
        self.assertEqual(post.description, 'Another Test Description')
        self.assertEqual(post.text, 'Another Test Text')
        self.assertEqual(post.category.count(), 1)

    def test_get_absolute_url(self):
        self.assertEqual(self.post.get_absolute_url(), reverse('Home:post-detail', args=[self.post.id, self.post.slug]))

    def test_get_related_posts_by_category(self):
        related_posts = self.post.get_related_posts_by_category()
        self.assertEqual(len(related_posts), 1)
        self.assertIn(self.post, related_posts)

    def test_save_creates_slug(self):
        self.post.save()
        self.assertEqual(self.post.slug, slugify(self.post.title, allow_unicode=True))

    def test_str_method(self):
        self.assertEqual(str(self.post), self.post.title)


class CommentModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(phone_number='09224201664', username='testuser', password='1234')
        self.category = Category.objects.create(name='Test Category')
        self.post = Post.objects.create(
            title='Test Post',
            image='posts/image/test_image.jpg',
            author=self.user,
            post_type='NORMAL',
            description='Test Description',
            text='Test Text'
        )
        self.post.category.set([self.category.pk])
        self.comment = Comment.objects.create(
            post=self.post,
            author=self.user,
            body='Test comment'
        )

    def test_create_comment(self):
        comment = Comment.objects.create(
            post=self.post,
            author=self.user,
            body='Another test comment'
        )
        self.assertEqual(comment.post, self.post)
        self.assertEqual(comment.author, self.user)
        self.assertEqual(comment.body, 'Another test comment')
        self.assertFalse(comment.is_reply)

    def test_create_reply(self):
        reply = Comment.objects.create(
            post=self.post,
            author=self.user,
            body='This is a reply',
            parent=self.comment,
            is_reply=True
        )
        self.assertEqual(reply.post, self.post)
        self.assertEqual(reply.author, self.user)
        self.assertEqual(reply.body, 'This is a reply')
        self.assertTrue(reply.is_reply)
        self.assertEqual(reply.parent, self.comment)

    def test_str_method_comment(self):
        self.assertEqual(str(self.comment), f'{self.comment.author} commented to {self.comment.post}')

    def test_str_method_reply(self):
        reply = Comment.objects.create(
            post=self.post,
            author=self.user,
            body='This is a reply',
            parent=self.comment,
            is_reply=True
        )
        self.assertEqual(str(reply), f'{reply.parent.author} replied to {reply.parent}')


class CategoryModelTest(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name='Main Category')
        self.subcategory = Category.objects.create(name='Sub Category', parent=self.category)

    def test_create_category(self):
        category = Category.objects.create(name='Another Main Category')
        self.assertEqual(category.name, 'Another Main Category')
        self.assertIsNone(category.parent)

    def test_create_subcategory(self):
        subcategory = Category.objects.create(name='Another Sub Category', parent=self.category)
        self.assertEqual(subcategory.name, 'Another Sub Category')
        self.assertEqual(subcategory.parent, self.category)

    def test_str_method_category(self):
        self.assertEqual(str(self.category), 'Main Category')


    def test_verbose_name(self):
        self.assertEqual(Category._meta.verbose_name, 'category')

    def test_verbose_name_plural(self):
        self.assertEqual(Category._meta.verbose_name_plural, 'categories')
