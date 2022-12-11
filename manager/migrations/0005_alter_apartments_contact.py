# Generated by Django 4.1.3 on 2022-11-27 06:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0004_alter_apartments_contact'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apartments',
            name='contact',
            field=models.ForeignKey(blank=True, limit_choices_to={'user_type': 'adm'}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='owners', to=settings.AUTH_USER_MODEL),
        ),
    ]
