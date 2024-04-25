# Generated by Django 5.0.1 on 2024-01-28 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('console', '0046_rename_file_events_cover_picture_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='contact_number',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='events',
            name='description',
            field=models.CharField(default='', max_length=500),
        ),
        migrations.AlterField(
            model_name='pre_wedding',
            name='description',
            field=models.CharField(default='', max_length=500),
        ),
        migrations.AlterField(
            model_name='wedding',
            name='description',
            field=models.CharField(default='', max_length=500),
        ),
    ]
