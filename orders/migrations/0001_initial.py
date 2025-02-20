# Generated by Django 5.1.1 on 2024-09-07 14:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Delivery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('fee', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='OrderDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('is_reviewed', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('fee', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField()),
                ('rating_point', models.DecimalField(decimal_places=2, max_digits=3)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('purchase_address', models.TextField()),
                ('delivery_address', models.TextField()),
                ('total_price_product', models.DecimalField(decimal_places=2, max_digits=10)),
                ('fee_payment', models.DecimalField(decimal_places=2, max_digits=10)),
                ('status', models.CharField(max_length=50)),
                ('note', models.TextField(blank=True)),
                ('phone_number', models.CharField(max_length=20)),
                ('full_name', models.CharField(max_length=256)),
                ('fee_delivery', models.DecimalField(decimal_places=2, max_digits=10)),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('status_payment', models.CharField(max_length=50)),
                ('status_delivery', models.CharField(max_length=50)),
                ('delivery', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='orders.delivery')),
            ],
        ),
    ]
