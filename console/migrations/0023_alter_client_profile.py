# Generated by Django 5.0.1 on 2024-01-22 01:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('console', '0022_alter_client_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='profile',
            field=models.FileField(blank=True, null=True, upload_to='assets/images/user/profile-picture'),
        ),
    ]