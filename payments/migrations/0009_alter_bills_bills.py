# Generated by Django 4.2.7 on 2023-12-02 19:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0008_remove_payments_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bills',
            name='bills',
            field=models.CharField(choices=[('Rent', 'Rent'), ('Electricity', 'Electricity'), ('Water', 'Water'), ('Internet', 'Internet'), ('Cable', 'Cable'), ('Others', 'Others')], max_length=100),
        ),
    ]
