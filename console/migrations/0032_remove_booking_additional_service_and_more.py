# Generated by Django 5.0.1 on 2024-01-25 02:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('console', '0031_booking_additional_service_booking_service'),
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
