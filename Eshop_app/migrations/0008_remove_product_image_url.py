# Generated by Django 5.1.1 on 2024-09-30 17:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Eshop_app', '0007_merge_20240930_1913'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='image_url',
        ),
    ]
