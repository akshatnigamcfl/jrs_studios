# Generated by Django 5.0.1 on 2024-03-25 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('console', '0093_events_created_at_pre_wedding_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='events',
            name='created_at',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='pre_wedding',
            name='created_at',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='reels',
            name='created_at',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='wedding',
            name='created_at',
            field=models.DateField(auto_now_add=True),
        ),
    ]
