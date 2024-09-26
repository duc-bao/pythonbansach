# Generated by Django 5.1.1 on 2024-09-07 14:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id_book', models.AutoField(primary_key=True, serialize=False)),
                ('name_book', models.CharField(max_length=256)),
                ('author', models.CharField(max_length=512)),
                ('isbn', models.CharField(blank=True, max_length=256, null=True)),
                ('list_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('sell_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('quantity', models.IntegerField()),
                ('description', models.TextField()),
                ('avg_rating', models.DecimalField(decimal_places=2, default=0, max_digits=3)),
                ('sold_quantity', models.IntegerField(default=0)),
                ('discount_percent', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id_category', models.AutoField(primary_key=True, serialize=False)),
                ('name_category', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='FavoriteBook',
            fields=[
                ('id_favorites_book', models.AutoField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id_image', models.AutoField(primary_key=True, serialize=False)),
                ('name_image', models.CharField(max_length=256)),
                ('is_thumbnail', models.BooleanField(default=False)),
                ('url_image', models.URLField(max_length=512)),
                ('data_image', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='BookCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.book')),
            ],
            options={
                'db_table': 'book_category',
            },
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id_cart', models.AutoField(primary_key=True, serialize=False)),
                ('quantity', models.IntegerField(default=1)),
                ('id_book', models.ForeignKey(db_column='id_book', on_delete=django.db.models.deletion.CASCADE, to='products.book')),
            ],
        ),
    ]
