# Generated by Django 4.2.20 on 2025-05-14 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ambulancemodel',
            name='link',
            field=models.CharField(default='https://www.google.com/', max_length=255),
        ),
        migrations.AddField(
            model_name='doctormodel',
            name='link',
            field=models.CharField(default='https://www.google.com/', max_length=255),
        ),
    ]
