from django.contrib import admin

# Register your models here.
from .models import Category, Product, ProductImage, Review,  Wishlist

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(Review)
admin.site.register(Wishlist)