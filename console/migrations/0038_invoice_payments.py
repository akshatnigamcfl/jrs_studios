# Generated by Django 5.0.1 on 2024-01-27 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('console', '0037_alter_additionalservice_charges_application'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_price', models.IntegerField()),
                ('discount', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Payments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('amount', models.IntegerField()),
            ],
        ),
    ]
