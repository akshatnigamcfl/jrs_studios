# Generated by Django 5.0.1 on 2024-02-23 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('console', '0086_client_client_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='profile',
            field=models.FileField(blank=True, default='assets/images/user/profile-picture/user.png', null=True, upload_to='assets/images/user/profile-picture'),
        ),
    ]
