# Generated by Django 5.0.1 on 2024-02-20 06:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('console', '0076_service_segment'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]
