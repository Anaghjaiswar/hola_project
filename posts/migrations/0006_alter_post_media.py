# Generated by Django 5.1.3 on 2024-12-01 10:51

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0005_post_saved_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='media',
            field=cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, verbose_name='media'),
        ),
    ]