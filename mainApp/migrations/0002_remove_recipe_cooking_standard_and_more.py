# Generated by Django 4.2.4 on 2023-08-11 06:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipe',
            name='cooking_standard',
        ),
        migrations.AlterField(
            model_name='recipe',
            name='ingredients',
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='menu_title',
            field=models.CharField(max_length=100),
        ),
    ]