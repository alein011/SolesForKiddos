# Generated by Django 3.2.7 on 2023-07-17 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0029_policy_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='policy',
            name='slug',
            field=models.CharField(max_length=200),
        ),
    ]
