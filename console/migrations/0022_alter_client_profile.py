# Generated by Django 5.0.1 on 2024-01-22 01:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('console', '0021_alter_client_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='profile',
            field=models.FileField(default='', upload_to='assets/images/user/profile-picture'),
            preserve_default=False,
        ),
    ]
