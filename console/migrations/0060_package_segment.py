# Generated by Django 5.0.1 on 2024-02-03 07:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('console', '0059_segment'),
    ]

    operations = [
        migrations.AddField(
            model_name='package',
            name='segment',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='console.segment'),
            preserve_default=False,
        ),
    ]
