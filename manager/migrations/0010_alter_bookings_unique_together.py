# Generated by Django 4.1.3 on 2022-11-27 16:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0009_alter_bookings_assigned'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='bookings',
            unique_together={('req_user', 'util', 'date', 'time')},
        ),
    ]