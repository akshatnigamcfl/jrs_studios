# Generated by Django 5.0.1 on 2024-02-21 04:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('console', '0079_additionalservice_trash'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='additionalservice',
            name='segment',
        ),
    ]
