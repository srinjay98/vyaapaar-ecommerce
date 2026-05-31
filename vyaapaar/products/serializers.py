from rest_framework import serializers
from .models import Category, Product, ProductImage


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class ProductImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductImage
        fields = ['id', 'image']


class ProductSerializer(serializers.ModelSerializer):

    images = ProductImageSerializer(
        many=True,
        read_only=True
    )

    seller = serializers.ReadOnlyField(
        source='seller.username'
    )

    class Meta:
        model = Product

        fields = [
            'id',
            'seller',
            'category',
            'name',
            'slug',
            'description',
            'price',
            'stock',
            'is_available',
            'images',
            'created_at'
        ]

class ProductImageUploadSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductImage

        fields = ['id', 'product', 'image']        