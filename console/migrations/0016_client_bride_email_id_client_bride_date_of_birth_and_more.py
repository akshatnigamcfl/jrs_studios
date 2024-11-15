# Generated by Django 5.0.1 on 2024-01-21 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('console', '0015_rename_wedding_date_client_main_wedding_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='bride_Email_id',
            field=models.CharField(blank=True, default='', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='client',
            name='bride_date_of_birth',
            field=models.CharField(blank=True, default='', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='client',
            name='bride_name',
            field=models.CharField(blank=True, default='', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='client',
            name='groom_Email_id',
            field=models.CharField(blank=True, default='', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='client',
            name='groom_contact_number',
            field=models.CharField(blank=True, default='', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='client',
            name='groom_date_of_birth',
            field=models.CharField(blank=True, default='', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='client',
            name='groom_name',
            field=models.CharField(blank=True, default='', max_length=100, null=True),
        ),
    ]
