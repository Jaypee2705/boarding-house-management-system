# Generated by Django 4.2.7 on 2023-12-02 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boardinghouse', '0003_boardinghouse_is_archive'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='is_archive',
            field=models.BooleanField(default=False),
        ),
    ]