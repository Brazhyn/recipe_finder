# Generated by Django 5.1.5 on 2025-01-20 19:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ingredient',
            name='description',
        ),
    ]
