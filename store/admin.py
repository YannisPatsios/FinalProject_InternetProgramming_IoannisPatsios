from django.contrib import admin
from .models import Category, Product, UserProfile, Review, Cart, CartItem, Order, OrderItem

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(UserProfile)
admin.site.register(Review)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)
