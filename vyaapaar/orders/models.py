from django.db import models

from accounts.models import User

from products.models import Product


class Order(models.Model):

    STATUS_CHOICES = (

        ('pending', 'Pending'),

        ('processing', 'Processing'),

        ('shipped', 'Shipped'),

        ('delivered', 'Delivered'),

        ('cancelled', 'Cancelled'),
    )

    buyer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='orders'
    )

    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    is_paid = models.BooleanField(default=False)

    def __str__(self):

        return f"Order {self.id}"


class OrderItem(models.Model):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField()

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def __str__(self):

        return self.product.name
    
class Payment(models.Model):

    PAYMENT_STATUS = (

        ('pending', 'Pending'),

        ('success', 'Success'),

        ('failed', 'Failed'),
    )

    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name='payment'
    )

    razorpay_order_id = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    razorpay_payment_id = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    razorpay_signature = models.CharField(
        max_length=500,
        blank=True,
        null=True
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS,
        default='pending'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"Payment {self.id}"    
    
class Coupon(models.Model):

    code = models.CharField(
        max_length=50,
        unique=True
    )

    discount_percent = models.PositiveIntegerField()

    active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return self.code    