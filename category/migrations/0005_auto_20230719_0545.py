# Generated by Django 3.2.7 on 2023-07-18 21:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0004_age'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='brand',
            name='description',
        ),
        migrations.RemoveField(
            model_name='category',
            name='cat_image',
        ),
        migrations.RemoveField(
            model_name='category',
            name='description',
        ),
    ]