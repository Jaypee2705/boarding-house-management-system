# Generated by Django 4.2.7 on 2023-11-28 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0003_payments'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payments',
            name='date',
            field=models.DateField(),
        ),
    ]
