# Generated by Django 5.0.1 on 2024-01-28 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('console', '0044_rename_youtube_pre_wedding_is_youtube_video'),
    ]

    operations = [
        migrations.RenameField(
            model_name='wedding',
            old_name='file',
            new_name='cover_picture',
        ),
        migrations.AddField(
            model_name='wedding',
            name='is_youtube_video',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='wedding',
            name='video_link',
            field=models.FileField(null=True, upload_to='assets/video/pre_wedding'),
        ),
        migrations.AddField(
            model_name='wedding',
            name='video_youtube_link',
            field=models.TextField(null=True),
        ),
    ]
