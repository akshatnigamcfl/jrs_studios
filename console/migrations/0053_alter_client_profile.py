# Generated by Django 5.0.1 on 2024-01-30 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('console', '0052_canned_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='profile',
            field=models.FileField(blank=True, default='/assets/images/user/profile-picture', null=True, upload_to='assets/images/user/profile-picture'),
        ),
    ]
