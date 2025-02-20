# Generated by Django 5.1.1 on 2024-09-15 12:03

import cloudinary_storage.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_user_options_alter_user_managers_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, null=True, storage=cloudinary_storage.storage.RawMediaCloudinaryStorage(), upload_to='avatars/'),
        ),
    ]
