# Generated by Django 3.2.7 on 2023-07-17 00:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0025_remove_faqs_ordernumber'),
    ]

    operations = [
        migrations.AlterField(
            model_name='faqs',
            name='status',
            field=models.CharField(choices=[('True', 'True'), ('False', 'False')], default=True, max_length=10),
        ),
    ]
