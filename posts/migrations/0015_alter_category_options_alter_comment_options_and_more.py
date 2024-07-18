# Generated by Django 5.0.6 on 2024-07-18 08:10

import ckeditor.fields
import django.db.models.deletion
import mptt.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0014_category_created_category_updated_comment_created_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'دسته بندی', 'verbose_name_plural': 'دسته بندی ها'},
        ),
        migrations.AlterModelOptions(
            name='comment',
            options={},
        ),
        migrations.AlterModelOptions(
            name='post',
            options={'verbose_name': 'پست', 'verbose_name_plural': 'پست ها'},
        ),
        migrations.RemoveField(
            model_name='category',
            name='created',
        ),
        migrations.RemoveField(
            model_name='category',
            name='updated',
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=70),
        ),
        migrations.AlterField(
            model_name='category',
            name='name_en',
            field=models.CharField(max_length=70, null=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='name_fa',
            field=models.CharField(max_length=70, null=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='parent',
            field=mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subs', to='posts.category'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ucomments', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='comment',
            name='body',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='comment',
            name='is_reply',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='comment',
            name='parent',
            field=mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='rcomments', to='posts.comment'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pcomments', to='posts.post'),
        ),
        migrations.AlterField(
            model_name='post',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='نویسنده'),
        ),
        migrations.AlterField(
            model_name='post',
            name='category',
            field=models.ManyToManyField(related_name='posts', to='posts.category'),
        ),
        migrations.AlterField(
            model_name='post',
            name='description',
            field=ckeditor.fields.RichTextField(verbose_name='توضیحات'),
        ),
        migrations.AlterField(
            model_name='post',
            name='description_en',
            field=ckeditor.fields.RichTextField(null=True, verbose_name='توضیحات'),
        ),
        migrations.AlterField(
            model_name='post',
            name='description_fa',
            field=ckeditor.fields.RichTextField(null=True, verbose_name='توضیحات'),
        ),
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(upload_to='posts/image/', verbose_name='تصویر'),
        ),
        migrations.AlterField(
            model_name='post',
            name='post_type',
            field=models.CharField(choices=[('NORMAL', 'معمولی'), ('VIP', 'ویژه')], default='NORMAL', max_length=6, verbose_name='نوع پست'),
        ),
        migrations.AlterField(
            model_name='post',
            name='slug',
            field=models.SlugField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='text',
            field=ckeditor.fields.RichTextField(verbose_name='متن'),
        ),
        migrations.AlterField(
            model_name='post',
            name='text_en',
            field=ckeditor.fields.RichTextField(null=True, verbose_name='متن'),
        ),
        migrations.AlterField(
            model_name='post',
            name='text_fa',
            field=ckeditor.fields.RichTextField(null=True, verbose_name='متن'),
        ),
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(max_length=100, verbose_name='عنوان'),
        ),
        migrations.AlterField(
            model_name='post',
            name='title_en',
            field=models.CharField(max_length=100, null=True, verbose_name='عنوان'),
        ),
        migrations.AlterField(
            model_name='post',
            name='title_fa',
            field=models.CharField(max_length=100, null=True, verbose_name='عنوان'),
        ),
    ]