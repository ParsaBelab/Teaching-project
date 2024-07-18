# Generated by Django 5.0.6 on 2024-07-14 11:55

import ckeditor.fields
import django.db.models.deletion
import mptt.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0012_category_name_en_category_name_fa'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'category', 'verbose_name_plural': 'categories'},
        ),
        migrations.AlterModelOptions(
            name='comment',
            options={'verbose_name': 'comment', 'verbose_name_plural': 'comments'},
        ),
        migrations.AlterModelOptions(
            name='post',
            options={'verbose_name': 'post', 'verbose_name_plural': 'posts'},
        ),
        migrations.RemoveField(
            model_name='comment',
            name='created',
        ),
        migrations.RemoveField(
            model_name='post',
            name='created',
        ),
        migrations.RemoveField(
            model_name='post',
            name='updated',
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=70, verbose_name='title'),
        ),
        migrations.AlterField(
            model_name='category',
            name='name_en',
            field=models.CharField(max_length=70, null=True, verbose_name='title'),
        ),
        migrations.AlterField(
            model_name='category',
            name='name_fa',
            field=models.CharField(max_length=70, null=True, verbose_name='title'),
        ),
        migrations.AlterField(
            model_name='category',
            name='parent',
            field=mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subs', to='posts.category', verbose_name='sub of'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ucomments', to=settings.AUTH_USER_MODEL, verbose_name='author'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='body',
            field=models.CharField(max_length=250, verbose_name='text'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='is_reply',
            field=models.BooleanField(default=False, verbose_name='is reply'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='parent',
            field=mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='rcomments', to='posts.comment', verbose_name='reply to'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pcomments', to='posts.post', verbose_name='post'),
        ),
        migrations.AlterField(
            model_name='post',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='author'),
        ),
        migrations.AlterField(
            model_name='post',
            name='category',
            field=models.ManyToManyField(related_name='posts', to='posts.category', verbose_name='category'),
        ),
        migrations.AlterField(
            model_name='post',
            name='description',
            field=ckeditor.fields.RichTextField(verbose_name='description'),
        ),
        migrations.AlterField(
            model_name='post',
            name='description_en',
            field=ckeditor.fields.RichTextField(null=True, verbose_name='description'),
        ),
        migrations.AlterField(
            model_name='post',
            name='description_fa',
            field=ckeditor.fields.RichTextField(null=True, verbose_name='description'),
        ),
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(upload_to='posts/image/', verbose_name='image'),
        ),
        migrations.AlterField(
            model_name='post',
            name='post_type',
            field=models.CharField(choices=[('NORMAL', 'normal'), ('VIP', 'VIP')], default='NORMAL', max_length=6, verbose_name='post_type'),
        ),
        migrations.AlterField(
            model_name='post',
            name='slug',
            field=models.SlugField(blank=True, null=True, verbose_name='slug'),
        ),
        migrations.AlterField(
            model_name='post',
            name='text',
            field=ckeditor.fields.RichTextField(verbose_name='text'),
        ),
        migrations.AlterField(
            model_name='post',
            name='text_en',
            field=ckeditor.fields.RichTextField(null=True, verbose_name='text'),
        ),
        migrations.AlterField(
            model_name='post',
            name='text_fa',
            field=ckeditor.fields.RichTextField(null=True, verbose_name='text'),
        ),
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(max_length=100, verbose_name='title'),
        ),
        migrations.AlterField(
            model_name='post',
            name='title_en',
            field=models.CharField(max_length=100, null=True, verbose_name='title'),
        ),
        migrations.AlterField(
            model_name='post',
            name='title_fa',
            field=models.CharField(max_length=100, null=True, verbose_name='title'),
        ),
    ]