# Generated by Django 5.0.6 on 2024-07-06 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_alter_user_full_name_alter_user_job_and_more'),
        ('posts', '0007_alter_category_options_post_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='favorites',
            field=models.ManyToManyField(blank=True, null=True, related_name='favorited_by', to='posts.post'),
        ),
    ]
