# Generated by Django 5.0.1 on 2024-02-20 04:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('console', '0073_remove_invoice_discount_remove_invoice_total_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='service',
            name='price',
        ),
    ]
