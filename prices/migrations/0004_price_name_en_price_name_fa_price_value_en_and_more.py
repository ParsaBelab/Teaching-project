# Generated by Django 5.0.6 on 2024-07-13 07:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prices', '0003_alter_price_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='price',
            name='name_en',
            field=models.CharField(max_length=50, null=True, verbose_name='عنوان'),
        ),
        migrations.AddField(
            model_name='price',
            name='name_fa',
            field=models.CharField(max_length=50, null=True, verbose_name='عنوان'),
        ),
        migrations.AddField(
            model_name='price',
            name='value_en',
            field=models.PositiveIntegerField(null=True, verbose_name='قیمت'),
        ),
        migrations.AddField(
            model_name='price',
            name='value_fa',
            field=models.PositiveIntegerField(null=True, verbose_name='قیمت'),
        ),
    ]