# Generated by Django 4.1.3 on 2022-11-27 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0015_remove_apartments_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apartments',
            name='contact',
            field=models.CharField(blank=True, max_length=12, null=True),
        ),
    ]
