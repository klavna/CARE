# Generated by Django 4.2.3 on 2023-08-15 10:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0011_rating_rating_rating_recipe_id_rating_user_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rating',
            name='rating',
        ),
        migrations.RemoveField(
            model_name='rating',
            name='recipe_id',
        ),
        migrations.RemoveField(
            model_name='rating',
            name='user_id',
        ),
    ]
