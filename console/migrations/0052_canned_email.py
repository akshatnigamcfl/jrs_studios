# Generated by Django 5.0.1 on 2024-01-30 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('console', '0051_alter_invoice_payment'),
    ]

    operations = [
        migrations.CreateModel(
            name='canned_email',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.TextField()),
                ('email_type', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
    ]
