# Generated by Django 5.0.6 on 2024-07-02 07:25

import phonenumber_field.modelfields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_user_phone_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='OTPCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None)),
                ('otp_code', models.PositiveSmallIntegerField()),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
