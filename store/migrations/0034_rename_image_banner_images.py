# Generated by Django 3.2.7 on 2023-07-17 19:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0033_alter_banner_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='banner',
            old_name='image',
            new_name='images',
        ),
    ]
