# Generated by Django 3.2.7 on 2023-07-15 05:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0014_variation_stock'),
    ]

    operations = [
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color', models.CharField(max_length=100)),
            ],
        ),
        migrations.RemoveField(
            model_name='variation',
            name='stock',
        ),
        migrations.AddField(
            model_name='product',
            name='colors',
            field=models.CharField(default='[]', max_length=200),
        ),
    ]