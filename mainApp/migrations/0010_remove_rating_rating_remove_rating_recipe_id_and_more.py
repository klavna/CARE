# Generated by Django 4.2.3 on 2023-08-15 09:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0009_rating_user_id'),
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
