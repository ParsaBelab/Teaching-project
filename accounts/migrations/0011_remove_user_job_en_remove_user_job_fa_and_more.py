# Generated by Django 5.0.6 on 2024-07-14 07:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_user_job_en_user_job_fa_user_username_en_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='job_en',
        ),
        migrations.RemoveField(
            model_name='user',
            name='job_fa',
        ),
        migrations.RemoveField(
            model_name='user',
            name='username_en',
        ),
        migrations.RemoveField(
            model_name='user',
            name='username_fa',
        ),
    ]
