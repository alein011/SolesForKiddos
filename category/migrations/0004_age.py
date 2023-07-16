# Generated by Django 3.2.7 on 2023-07-13 20:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0003_brand_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='Age',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('age', models.CharField(max_length=50, unique=True)),
                ('slug', models.SlugField(max_length=100, unique=True)),
            ],
        ),
    ]