# Generated by Django 5.0.1 on 2024-04-01 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('console', '0098_remove_client_qoutation_delete_quotation'),
    ]

    operations = [
        migrations.CreateModel(
            name='Deliverables',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=50, null=True)),
                ('trash', models.BooleanField(default=False)),
            ],
        ),
    ]
