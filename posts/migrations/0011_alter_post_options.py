# Generated by Django 5.0.6 on 2024-07-13 07:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0010_alter_post_options_post_description_en_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'verbose_name': 'پست', 'verbose_name_plural': 'پست ها'},
        ),
    ]