# django apps
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

# local apps
from accounts.models import User
from utils.abstracts import AbstractDateTime

# third-party apps
from ckeditor.fields import RichTextField
from mptt.models import MPTTModel, TreeForeignKey


class Post(AbstractDateTime, models.Model):
    POST_TYPES = (
        ('NORMAL', _('normal')),
        ('VIP', _('VIP')),
    )

    title = models.CharField(
        max_length=100,
        verbose_name=_('title')
    )
    image = models.ImageField(
        upload_to='posts/image/',
        verbose_name=_('image')
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('author')
    )
    post_type = models.CharField(
        max_length=6,
        choices=POST_TYPES,
        default='NORMAL',
        verbose_name=_('post_type')
    )
    category = models.ManyToManyField(
        'Category',
        related_name='posts',
        verbose_name='category'
    )
    description = RichTextField(
        verbose_name=_('description')
    )
    text = RichTextField(
        verbose_name=_('text')
    )
    slug = models.SlugField(
        blank=True,
        null=True,
        verbose_name='slug'
    )

    def get_absolute_url(self):
        return reverse('Home:post-detail', args=[self.id, self.slug])

    def get_related_posts_by_category(self):
        posts = Post.objects.filter(category__in=self.category.all()).distinct()[:10]
        return posts

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.slug = slugify(self.title, allow_unicode=True)
        super(Post, self).save()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('post')
        verbose_name_plural = _('posts')


class Comment(AbstractDateTime,MPTTModel):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='pcomments',
        verbose_name=_('post')
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='ucomments',
        verbose_name=_('author')
    )
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='rcomments',
        verbose_name=_('reply to'),
        null=True,
        blank=True
    )
    is_reply = models.BooleanField(
        default=False,
        verbose_name=_('is reply')
    )
    body = models.CharField(
        max_length=250,
        verbose_name='text',
    )

    def __str__(self):
        if self.is_reply:
            return f'{self.parent.author} replied to {self.parent}'
        else:
            return f'{self.author} commented to {self.post}'

    class MPTTMeta:
        order_insertion_by = ['-created']

    class Meta:
        verbose_name = _('comment')
        verbose_name_plural = _('comments')


class Category(AbstractDateTime,MPTTModel):
    name = models.CharField(
        max_length=70,
        verbose_name=_('title')
    )
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='subs',
        verbose_name=_('sub of')
    )

    class Meta:
        verbose_name_plural = _('categories')
        verbose_name = _('category')

    def __str__(self):
        if self.parent:
            return _(f'{self.name} is sub category of {self.parent}')
        else:
            return self.name
