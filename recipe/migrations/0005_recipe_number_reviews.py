# Generated by Django 5.1.5 on 2025-01-23 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0004_recipe_avg_rating_alter_review_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='number_reviews',
            field=models.IntegerField(default=0),
        ),
    ]
