# Generated by Django 5.1.1 on 2024-09-15 16:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderdetail',
            name='is_reviewed',
        ),
        migrations.DeleteModel(
            name='Review',
        ),
    ]
