from rest_framework import serializers

from .models import Order, OrderItem, Payment


class OrderItemSerializer(serializers.ModelSerializer):

    product_name = serializers.CharField(
        source='product.name',
        read_only=True
    )

    class Meta:

        model = OrderItem

        fields = [
            'id',
            'product',
            'product_name',
            'quantity',
            'price'
        ]


class OrderSerializer(serializers.ModelSerializer):

    items = OrderItemSerializer(
        many=True,
        read_only=True
    )

    class Meta:

        model = Order

        fields = [
            'id',
            'buyer',
            'total_amount',
            'status',
            'items',
            'created_at'
        ]

class PaymentSerializer(serializers.ModelSerializer):

    class Meta:

        model = Payment

        fields = '__all__'        