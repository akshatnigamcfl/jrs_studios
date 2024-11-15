# Generated by Django 5.0.1 on 2024-01-24 09:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('console', '0025_additionalservice_alter_booking_shoot_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='additional_service',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='console.additionalservice'),
        ),
        migrations.AlterField(
            model_name='booking',
            name='service',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='console.service'),
        ),
    ]
