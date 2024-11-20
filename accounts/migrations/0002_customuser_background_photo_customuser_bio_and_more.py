# Generated by Django 5.1.3 on 2024-11-19 21:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='background_photo',
            field=models.ImageField(blank=True, null=True, upload_to='background_photos/'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='bio',
            field=models.TextField(blank=True, max_length=500),
        ),
        migrations.AddField(
            model_name='customuser',
            name='profile_photo',
            field=models.ImageField(blank=True, null=True, upload_to='profile_photos/'),
        ),
    ]
