# Generated by Django 5.0.1 on 2024-02-08 15:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('console', '0060_package_segment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='package',
        ),
        migrations.AddField(
            model_name='booking',
            name='package',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='console.package'),
        ),
    ]
