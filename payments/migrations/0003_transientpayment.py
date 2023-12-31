# Generated by Django 4.2.7 on 2023-12-12 18:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('boardinghouse', '0001_initial'),
        ('payments', '0002_alter_bills_bills_alter_payments_amount'),
    ]

    operations = [
        migrations.CreateModel(
            name='TransientPayment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transient', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=100)),
                ('contact', models.CharField(max_length=100)),
                ('days', models.IntegerField(default=0)),
                ('amount', models.CharField(max_length=100)),
                ('note', models.CharField(blank=True, max_length=100, null=True)),
                ('mode', models.CharField(blank=True, max_length=100, null=True)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='boardinghouse.room')),
            ],
        ),
    ]
