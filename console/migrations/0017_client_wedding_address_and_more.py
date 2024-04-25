# Generated by Django 5.0.1 on 2024-01-21 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('console', '0016_client_bride_email_id_client_bride_date_of_birth_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='wedding_address',
            field=models.CharField(blank=True, default='', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='client',
            name='bride_date_of_birth',
            field=models.DateField(blank=True, default='0001-01-01', null=True),
        ),
        migrations.AlterField(
            model_name='client',
            name='groom_date_of_birth',
            field=models.DateField(blank=True, default='0001-01-01', null=True),
        ),
    ]
