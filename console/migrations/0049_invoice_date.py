# Generated by Django 5.0.1 on 2024-01-29 05:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('console', '0048_alter_pre_wedding_video_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='date',
            field=models.DateField(auto_now_add=True, default='0001-01-01'),
            preserve_default=False,
        ),
    ]
