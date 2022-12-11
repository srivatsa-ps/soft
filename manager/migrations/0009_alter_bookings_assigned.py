# Generated by Django 4.1.3 on 2022-11-27 16:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0008_alter_bookings_date_alter_bookings_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookings',
            name='assigned',
            field=models.ForeignKey(limit_choices_to={'user_type': 'emp'}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='jobs', to=settings.AUTH_USER_MODEL),
        ),
    ]
