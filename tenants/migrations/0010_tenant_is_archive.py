# Generated by Django 4.2.7 on 2023-12-02 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tenants', '0009_alter_tenant_date_start'),
    ]

    operations = [
        migrations.AddField(
            model_name='tenant',
            name='is_archive',
            field=models.BooleanField(default=False),
        ),
    ]