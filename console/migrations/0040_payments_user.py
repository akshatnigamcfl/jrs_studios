# Generated by Django 5.0.1 on 2024-01-27 13:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('console', '0039_invoice_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='payments',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='console.client'),
            preserve_default=False,
        ),
    ]
