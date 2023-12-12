# Generated by Django 4.2.7 on 2023-12-12 16:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('boardinghouse', '0001_initial'),
        ('tenants', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=100, max_length=100)),
                ('date', models.DateField(auto_now_add=True)),
                ('note', models.CharField(blank=True, max_length=100, null=True)),
                ('mode', models.CharField(blank=True, max_length=100, null=True)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='boardinghouse.room')),
                ('tenant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tenants.tenant')),
            ],
        ),
        migrations.CreateModel(
            name='Bills',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bills', models.DecimalField(decimal_places=2, max_digits=100, max_length=100)),
                ('rate', models.CharField(max_length=100)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='boardinghouse.room')),
            ],
        ),
    ]
