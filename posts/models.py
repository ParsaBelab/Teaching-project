from django.db import models
from ckeditor.fields import RichTextField
from django.urls import reverse
from django.utils.text import slugify

from accounts.models import User
from mptt.models import MPTTModel, TreeForeignKey


class Post(models.Model):
    POST_TYPES = (
        ('NORMAL', 'معمولی'),
        ('VIP', 'ویژه'),
    )

    title = models.CharField(max_length=100, verbose_name='عنوان')
    image = models.ImageField(upload_to='posts/image/', verbose_name='تصویر')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='نویسنده')
    post_type = models.CharField(max_length=6, choices=POST_TYPES, default='NORMAL', verbose_name='نوع پست')
    category = models.ManyToManyField('Category', related_name='posts')
    description = RichTextField(verbose_name='توضیحات')
    text = RichTextField(verbose_name='متن')
    created = models.DateTimeField(auto_now_add=True, verbose_name='ایجاد')
    updated = models.DateTimeField(auto_now=True, verbose_name='آپدیت')
    slug = models.SlugField(blank=True, null=True)

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
        verbose_name = 'پست'
        verbose_name_plural = 'پست ها'


class Comment(MPTTModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='pcomments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ucomments')
    parent = TreeForeignKey('self', on_delete=models.CASCADE, related_name='rcomments',
                            null=True, blank=True)
    is_reply = models.BooleanField(default=False)
    body = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.is_reply:
            return f'{self.parent.author} replied to {self.parent}'
        else:
            return f'{self.author} commented to {self.post}'

    class MPTTMeta:
        order_insertion_by = ['-created']


class Category(MPTTModel):
    name = models.CharField(max_length=70)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='subs')

    class Meta:
        verbose_name_plural = 'دسته بندی ها'
        verbose_name = 'دسته بندی'

    def __str__(self):
        if self.parent:
            return f'{self.name} is sub category of {self.parent}'
        else:
            return self.name
