# Generated by Django 4.2.7 on 2023-11-28 16:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('boardinghouse', '0002_room_owner'),
        ('homepage', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('notice', models.TextField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('boardinghouse', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='boardinghouse.boardinghouse')),
            ],
        ),
    ]