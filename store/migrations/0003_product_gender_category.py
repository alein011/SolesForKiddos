# Generated by Django 4.2.1 on 2023-06-18 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_variation'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='gender_category',
            field=models.CharField(blank=True, choices=[('boys', 'boys'), ('girls', 'girls')], max_length=100),
        ),
    ]
