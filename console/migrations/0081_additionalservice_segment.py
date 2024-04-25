# Generated by Django 5.0.1 on 2024-02-21 04:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('console', '0080_remove_additionalservice_segment'),
    ]

    operations = [
        migrations.AddField(
            model_name='additionalservice',
            name='segment',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='console.segment'),
            preserve_default=False,
        ),
    ]