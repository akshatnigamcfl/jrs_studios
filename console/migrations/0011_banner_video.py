# Generated by Django 5.0.1 on 2024-01-16 02:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('console', '0010_alter_events_file'),
    ]

    operations = [
        migrations.CreateModel(
            name='Banner_video',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=50)),
                ('file', models.FileField(upload_to='assets/videos/Banner_video')),
            ],
        ),
    ]