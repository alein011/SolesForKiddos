# Generated by Django 3.2.7 on 2023-07-17 19:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0030_alter_policy_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='store/banner')),
                ('title', models.CharField(blank=True, max_length=20)),
                ('sub_title', models.CharField(blank=True, max_length=20)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.AlterModelOptions(
            name='faq_topic',
            options={'verbose_name': 'faq_topic', 'verbose_name_plural': 'FAQ Category'},
        ),
        migrations.AlterModelOptions(
            name='faqs',
            options={'verbose_name': 'faqs', 'verbose_name_plural': 'FAQ'},
        ),
        migrations.AlterModelOptions(
            name='policy',
            options={'verbose_name': 'policy', 'verbose_name_plural': 'policies'},
        ),
    ]