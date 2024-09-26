import base64
import binascii
import logging
import re

import cloudinary
from django.core.files.base import ContentFile
from rest_framework import serializers
from .models import Book, Category, Image, CartItem

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id_image', 'name_image', 'is_thumbnail', 'url_image', 'data_image', 'id_book']

class BookSerializer(serializers.ModelSerializer):
    # categories = CategorySerializer(many=True, read_only=True)
    # images = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = Book
        fields = '__all__'

# class FavoriteBookSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = FavoriteBook
#         fields = '__all__'

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = '__all__'
class BookSerializer1(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = Book
        fields = [
            'id_book', 'name_book', 'author', 'isbn', 'list_price',
            'sell_price', 'quantity', 'description', 'avg_rating',
            'sold_quantity', 'discount_percent', 'categories'
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        # Rename fields to match the desired output
        field_mapping = {
            'id_book': 'idBook',
            'name_book': 'nameBook',
            'list_price': 'listPrice',
            'sell_price': 'sellPrice',
            'avg_rating': 'avgRating',
            'sold_quantity': 'soldQuantity',
            'discount_percent': 'discountPercent'
        }

        for old_key, new_key in field_mapping.items():
            if old_key in representation:
                representation[new_key] = representation.pop(old_key)

        # Format numeric fields
        numeric_fields = ['listPrice', 'sellPrice', 'avgRating', 'discountPercent']
        for field in numeric_fields:
            if field in representation and representation[field] is not None:
                representation[field] = float(representation[field])

        # Ensure ISBN is always a string
        representation['ISBN'] = representation.pop('isbn', '') or ''

        # Remove categories if it's an empty list
        if not representation['categories']:
            representation.pop('categories')

        return representation

class CustomBookSerializer(serializers.ModelSerializer):
    nameBook = serializers.CharField(source='name_book')
    listPrice = serializers.DecimalField(source='list_price', max_digits=10, decimal_places=2)
    sellPrice = serializers.DecimalField(source='sell_price', max_digits=10, decimal_places=2)
    avgRating = serializers.FloatField(source='avg_rating', allow_null=True)
    soldQuantity = serializers.IntegerField(source='sold_quantity', allow_null=True)
    discountPercent = serializers.IntegerField(source='discount_percent')
    idGenres = serializers.ListField(child=serializers.IntegerField(), write_only=True)
    thumbnail = serializers.CharField(write_only=True)
    relatedImg = serializers.ListField(child=serializers.CharField(), write_only=True)
    ISBN = serializers.CharField(source="isbn", required=False, allow_null=True, default="a")
    class Meta:
        model = Book
        fields = ['nameBook', 'author', 'listPrice', 'sellPrice', 'quantity', 'description',
                  'avgRating', 'soldQuantity', 'discountPercent', 'idGenres', 'thumbnail', 'relatedImg', 'ISBN']

    def create(self, validated_data):
        logging.info("Starting create method")
        genres_data = validated_data.pop('idGenres')
        thumbnail_data = validated_data.pop('thumbnail', None)
        related_img_data = validated_data.pop('relatedImg', [])

        logging.info(f"Creating book with data: {validated_data}")
        book = Book.objects.create(**validated_data)
        logging.info(f"Book created with ID: {book.id_book}")

        logging.info(f"Setting categories: {genres_data}")
        categories = Category.objects.filter(id_category__in=genres_data)
        book.categories.set(categories)

        if thumbnail_data:
            logging.info("Saving thumbnail")
            self._save_image(book, thumbnail_data, is_thumbnail=True)

        logging.info(f"Saving {len(related_img_data)} related images")
        for idx, img_data in enumerate(related_img_data):
            self._save_image(book, img_data, is_thumbnail=False, idx=idx)

        logging.info("Book creation complete")
        return book

    def update(self, instance, validated_data):
        genres_data = validated_data.pop('idGenres', None)
        thumbnail_data = validated_data.pop('thumbnail', None)
        related_img_data = validated_data.pop('relatedImg', None)

        # Update Book fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update categories if provided
        if genres_data is not None:
            categories = Category.objects.filter(id_category__in=genres_data)
            instance.categories.set(categories)

        # Update thumbnail if provided
        if thumbnail_data:
            self._save_image(instance, thumbnail_data, is_thumbnail=True)

        # Update related images if provided
        if related_img_data is not None:
            # Delete existing related images
            Image.objects.filter(id_book=instance, is_thumbnail=False).delete()
            # Save new related images
            for idx, img_data in enumerate(related_img_data):
                self._save_image(instance, img_data, is_thumbnail=False, idx=idx)

        return instance

    def _save_image(self, book, img_data, is_thumbnail=False, idx=None):
        try:
            # Clean the base64 string
            img_data = re.sub(r'^data:image/.+;base64,', '', img_data)
            img_data = img_data.strip()  # Remove any whitespace

            # Add padding if necessary
            img_data += '=' * (-len(img_data) % 4)

            # Decode the base64 string
            image_data = base64.b64decode(img_data)

            # Create a temporary file-like object
            temp_image = ContentFile(image_data)

            # Upload to Cloudinary
            result = cloudinary.uploader.upload(temp_image)

            # Get the Cloudinary URL
            cloudinary_url = result['secure_url']

            image, created = Image.objects.get_or_create(
                id_book=book,
                is_thumbnail=is_thumbnail,
                defaults={
                    'name_image': f'Book_{book.id_book}_{"thumb" if is_thumbnail else idx}',
                    'url_image': cloudinary_url,
                    'data_image': img_data
                }
            )

            if not created:
                # If updating an existing image, delete the old image from Cloudinary
                if image.url_image:
                    try:
                        # Extract public_id from the old URL
                        old_public_id = image.url_image.split('/')[-1].split('.')[0]
                        cloudinary.uploader.destroy(old_public_id)
                    except Exception:
                        pass  # If deletion fails, we'll just overwrite

                image.name_image = f'Book_{book.id_book}_{"thumb" if is_thumbnail else idx}'
                image.url_image = cloudinary_url
                image.data_image = img_data
                image.save()

        except binascii.Error as e:
            raise serializers.ValidationError(f"Invalid base64 string for image: {str(e)}")
        except Exception as e:
            raise serializers.ValidationError(f"Error processing image: {str(e)}")
class CategorySerializer1(serializers.ModelSerializer):
    idCategory = serializers.IntegerField(source='id_category', required=False)
    nameCategory = serializers.CharField(source='name_category')

    class Meta:
        model = Category
        fields = ['idCategory', 'nameCategory']
    def create(self, validated_data):
        return Category.objects.create(name_category=validated_data['name_category'])

    def update(self, instance, validated_data):
        instance.name_category = validated_data.get('name_category', instance.name_category)
        instance.save()
        return instance