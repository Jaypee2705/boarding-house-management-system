# Generated by Django 4.2.7 on 2023-11-30 17:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0007_payments_image_payments_mode'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payments',
            name='image',
        ),
    ]