# Generated by Django 5.0.1 on 2024-04-06 05:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('console', '0105_payments_payment_mode'),
    ]

    operations = [
        migrations.AddField(
            model_name='payments',
            name='payment_note',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]