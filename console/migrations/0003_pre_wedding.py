# Generated by Django 5.0.1 on 2024-01-13 05:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('console', '0002_rename_file_reels'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pre_Wedding',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('couple', models.CharField(default='', max_length=50)),
                ('description', models.CharField(default='', max_length=50)),
                ('date', models.DateField(default='0000-00-00')),
                ('poster', models.FileField(upload_to='assets/images/pre_wedding_poster')),
            ],
        ),
    ]
