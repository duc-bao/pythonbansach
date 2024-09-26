from django.db import models
from users.models import User

class Category(models.Model):
    id_category = models.AutoField(primary_key=True)  # To match SQL inserts with 'id_category'
    name_category = models.CharField(max_length=100)  # Renamed to 'name_category' to match SQL

    def __str__(self):
        return self.name_category

class Book(models.Model):
    id_book = models.AutoField(primary_key=True)
    name_book = models.CharField(max_length=256)  # Renamed to 'name_book' to match SQL
    author = models.CharField(max_length=512)
    isbn = models.CharField(max_length=256, null=True, blank=True)  # Allow NULL values to match SQL
    list_price = models.DecimalField(max_digits=10, decimal_places=2)
    sell_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    description = models.TextField()
    avg_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    sold_quantity = models.IntegerField(default=0)
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    categories = models.ManyToManyField(Category, through='BookCategory')

    def __str__(self):
        return self.name_book
    def to_dict(self):
        return {
            'idBook': self.id_book,
            'nameBook': self.name_book,
            'author': self.author,
            'listPrice': self.list_price,
            'sellPrice': str(self.sell_price),  # Convert Decimal to string
            'quantity': self.quantity,
            'soldQuantity': self.sold_quantity,
        }
class BookCategory(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        db_table = 'book_category'
        unique_together = (('book', 'category'),)

class Image(models.Model):
    id_image = models.AutoField(primary_key=True)  # To match SQL inserts with 'id_image'
    name_image = models.CharField(max_length=256)
    is_thumbnail = models.BooleanField(default=False)
    url_image = models.URLField(max_length=512)
    data_image = models.TextField()  # To match SQL data
    id_book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='images', db_column='id_book')

    def __str__(self):
        return f"{self.name_image} - {self.id_book.name_book}"

# class FavoriteBook(models.Model):
#     id_favorites_book = models.AutoField(primary_key=True)  # To match SQL inserts
#     id_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorite_books', db_column='id_user')
#     id_book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='favorited_by', db_column='id_book')
#
#     class Meta:
#         unique_together = ('id_user', 'id_book')
#
#     def __str__(self):
#         return f"{self.id_user.username} - {self.id_book.name_book}"

class CartItem(models.Model):
    id_cart = models.AutoField(primary_key=True)
    quantity = models.IntegerField(default=1)
    id_book = models.ForeignKey(Book, on_delete=models.CASCADE, db_column='id_book')
    id_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_items', db_column='id_user')

    def __str__(self):
        return f"{self.id_user.username} - {self.id_book.name_book} ({self.quantity})"

    class Meta:
        db_table = 'cart_item'
