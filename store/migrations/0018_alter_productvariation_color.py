# Generated by Django 3.2.7 on 2023-07-15 05:53

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0017_alter_productvariation_color'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productvariation',
            name='color',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('black', 'black'), ('white', 'white')], max_length=11),
        ),
    ]
