from django.db import models

# Create your models here.

# Import the built-in User model for ForeignKey
# This will be upgraded to Custom User model
from django.contrib.auth.models import User

# Each category of products in the e-commerce platform
class Category(models.Model):
    name = models.CharField(max_length=100)  # Category name

    def __str__(self):
        # String representation of the Category model, which will display the category name
        return self.name

# Product details within the e-commerce platform
class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  # Links to a Category
    name = models.CharField(max_length=200)  # Product name
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Product price with two decimal places
    description = models.TextField()  # A detailed description of the product
    image = models.ImageField(upload_to='products/')  # Image of the product, stored in the 'products/' directory

    def __str__(self):
        # String representation of the Product model, which will display the product name
        return self.name

# Order details for each purchase made on the e-commerce platform
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Links to the User who made the order
    products = models.ManyToManyField(Product, through='OrderItem')  # Many-to-many relationship to Products
    total_price = models.DecimalField(max_digits=10, decimal_places=2)  # Total price for the order
    ordered_date = models.DateTimeField(auto_now_add=True)  # Date when the order was placed, set automatically
    is_ordered = models.BooleanField(default=False)  # Status of the order (False if in cart, True if ordered)

    def __str__(self):
        # String representation of the Order model, displaying a unique identifier for each order
        return f"Order {self.id}"

# Intermediate model for Order and Product relationship, specifying quantity for each product in an order
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)  # Links to an Order
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Links to a Product
    quantity = models.PositiveIntegerField(default=1)  # Quantity of the product in the order

    def __str__(self):
        # String representation of the OrderItem model, displaying product name and quantity
        return f"{self.product.name} - {self.quantity}"
