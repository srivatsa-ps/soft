# Generated by Django 4.1.3 on 2022-11-27 19:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0014_apartments_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='apartments',
            name='price',
        ),
    ]