# Generated by Django 3.2.7 on 2023-07-17 20:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0038_banner_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='banner',
            name='images',
            field=models.ImageField(max_length=255, upload_to='photos/banners'),
        ),
    ]
