from django.db import models
from django.contrib.auth.models import User

# Category model for organizing products (supports subcategories)
class Category(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='subcategories', on_delete=models.CASCADE)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

# Product model for SDRs and accessories
class Product(models.Model):
    CATEGORY_CHOICES = [
        ('USB Dongles', 'USB Dongles'),
        ('Antennas', 'Antennas'),
        ('Software Tools', 'Software Tools'),
        ('Amplifiers', 'Amplifiers'),
        ('Decoders', 'Decoders'),
        ('Other', 'Other'),
    ]
    name = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='products/')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    brand = models.CharField(max_length=100)
    frequency_range = models.CharField(max_length=100)
    supported_protocols = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

# UserProfile extends Django's User for dashboard, wishlist, etc.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    wishlist = models.ManyToManyField(Product, blank=True, related_name='wishlisted_by')
    # Add more fields as needed (e.g., avatar, bio)

    def __str__(self):
        return self.user.username

# Review model for product ratings and reviews
class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField()  # 1-5 stars
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('product', 'user')  # One review per user per product

    def __str__(self):
        return f"{self.user.username} - {self.product.name} ({self.rating}★)"

# Cart model for shopping cart simulation
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart of {self.user.username}"

# CartItem model for items in a user's cart
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

# Order model for simulated purchases
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='OrderItem')
    created_at = models.DateTimeField(auto_now_add=True)
    confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"

# OrderItem model for products in an order
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} (Order #{self.order.id})"
