# Generated by Django 5.0.6 on 2024-07-14 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prices', '0005_alter_price_options_alter_price_days_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='price',
            options={'ordering': ('days',), 'verbose_name': 'Plan', 'verbose_name_plural': 'Plans'},
        ),
        migrations.AlterField(
            model_name='price',
            name='name',
            field=models.CharField(max_length=50, verbose_name='title'),
        ),
        migrations.AlterField(
            model_name='price',
            name='name_en',
            field=models.CharField(max_length=50, null=True, verbose_name='title'),
        ),
        migrations.AlterField(
            model_name='price',
            name='name_fa',
            field=models.CharField(max_length=50, null=True, verbose_name='title'),
        ),
    ]