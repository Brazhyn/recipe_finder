# Generated by Django 5.1.5 on 2025-02-21 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="phone",
            field=models.CharField(blank=True, default="0000000000", max_length=15),
        ),
    ]
