# Generated by Django 5.0.1 on 2024-01-24 13:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('console', '0029_remove_booking_additional_service_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='additional_service',
        ),
        migrations.RemoveField(
            model_name='booking',
            name='service',
        ),
    ]