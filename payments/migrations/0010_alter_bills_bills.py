# Generated by Django 4.2.7 on 2023-12-02 19:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0009_alter_bills_bills'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bills',
            name='bills',
            field=models.CharField(max_length=100),
        ),
    ]