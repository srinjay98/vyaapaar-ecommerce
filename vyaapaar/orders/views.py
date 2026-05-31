from django.shortcuts import render

# Create your views here.
from rest_framework import generics, status

from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated

from .models import Order, OrderItem, Payment

from .serializers import OrderSerializer

from cart.models import Cart

from products.models import Product

import razorpay

from django.conf import settings

from .serializers import PaymentSerializer

from rest_framework.views import APIView

from django.http import HttpResponse

from reportlab.pdfgen import canvas

from django.core.mail import send_mail

from .tasks import send_order_email

client = razorpay.Client(
    auth=(
        settings.RAZORPAY_KEY_ID,
        settings.RAZORPAY_KEY_SECRET
    )
)


class PlaceOrderView(generics.CreateAPIView):

    serializer_class = OrderSerializer

    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):

        try:

            cart = Cart.objects.get(
                user=request.user
            )

        except Cart.DoesNotExist:

            return Response(
                {
                    'error': 'Cart not found'
                },
                status=status.HTTP_404_NOT_FOUND
            )

        cart_items = cart.items.all()

        if not cart_items.exists():

            return Response(
                {
                    'error': 'Cart is empty'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        order = Order.objects.create(
            buyer=request.user
        )

        total_amount = 0

        for item in cart_items:

            product = item.product

            # Check stock availability
            if item.quantity > product.stock:

                return Response(
                    {
                        'error': (
                            f'Insufficient stock for '
                            f'{product.name}'
                        )
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Create order item
            OrderItem.objects.create(

                order=order,

                product=product,

                quantity=item.quantity,

                price=product.price
            )

            # Reduce stock
            product.stock -= item.quantity

            # Mark unavailable if stock becomes zero
            if product.stock == 0:

                product.is_available = False

            product.save()

            total_amount += (
                product.price * item.quantity
            )

        order.total_amount = total_amount

        order.save()

        send_order_email.delay(
            request.user.email,
            order.id
        )
        # send_mail(

        #           subject='Order Confirmation - ApnaCart',

        #           message=(
        #               f'Your order #{order.id} '
        #               f'has been placed successfully.'
        #           ),

        #           from_email=settings.EMAIL_HOST_USER,

        #           recipient_list=[request.user.email],

        #           fail_silently=False,
        #       )

        # Clear cart after order placement
        cart_items.delete()

        serializer = self.get_serializer(order)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )


class OrderListView(generics.ListAPIView):

    serializer_class = OrderSerializer

    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        return Order.objects.filter(
            buyer=self.request.user
        )


class CreatePaymentView(generics.CreateAPIView):

    serializer_class = PaymentSerializer

    permission_classes = [IsAuthenticated]

    def post(self, request, order_id):

        print("========== DEBUG ==========")
        print("USER:", request.user)
        print("AUTH:", request.auth)
        print("HEADERS:", request.headers.get("Authorization"))
        print("===========================")
        try:

            order = Order.objects.get(
                id=order_id
            )

        except Order.DoesNotExist:

            return Response(
                {
                    'error': 'Order not found'
                },
                status=status.HTTP_404_NOT_FOUND
            )

        amount = int(order.total_amount * 100)

        razorpay_order = client.order.create({

            'amount': amount,

            'currency': 'INR',

            'payment_capture': '1'
        })

        payment = Payment.objects.create(

            order=order,

            razorpay_order_id=razorpay_order['id'],

            amount=order.total_amount
        )

        return Response({

            'payment_id': payment.id,

            'razorpay_order_id': razorpay_order['id'],

            'amount': amount,

            'key': settings.RAZORPAY_KEY_ID
        })


class VerifyPaymentView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        razorpay_order_id = request.data.get(
            'razorpay_order_id'
        )

        razorpay_payment_id = request.data.get(
            'razorpay_payment_id'
        )

        razorpay_signature = request.data.get(
            'razorpay_signature'
        )

        try:

            payment = Payment.objects.get(
                razorpay_order_id=razorpay_order_id
            )

        except Payment.DoesNotExist:

            return Response(
                {
                    'error': 'Payment not found'
                },
                status=status.HTTP_404_NOT_FOUND
            )

        try:

            client.utility.verify_payment_signature({

                'razorpay_order_id': razorpay_order_id,

                'razorpay_payment_id': razorpay_payment_id,

                'razorpay_signature': razorpay_signature
            })

            payment.razorpay_payment_id = (
                razorpay_payment_id
            )

            payment.razorpay_signature = (
                razorpay_signature
            )

            payment.status = 'success'

            payment.save()

            payment.order.is_paid = True

            payment.order.save()

            return Response({

                'message': (
                    'Payment verified successfully'
                )
            })

        except:

            payment.status = 'failed'

            payment.save()

            return Response(
                {
                    'error': (
                        'Payment verification failed'
                    )
                },
                status=status.HTTP_400_BAD_REQUEST
            )


class GenerateInvoiceView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, order_id):

        try:

            order = Order.objects.get(
                id=order_id,
                buyer=request.user
            )

        except Order.DoesNotExist:

            return Response(
                {
                    'error': 'Order not found'
                },
                status=status.HTTP_404_NOT_FOUND
            )

        response = HttpResponse(
            content_type='application/pdf'
        )

        response[
            'Content-Disposition'
        ] = f'attachment; filename="invoice_{order.id}.pdf"'

        pdf = canvas.Canvas(response)

        # Title
        pdf.setFont("Helvetica-Bold", 18)

        pdf.drawString(
            200,
            800,
            "ApnaCart Invoice"
        )

        # Order details
        pdf.setFont("Helvetica", 12)

        pdf.drawString(
            50,
            750,
            f"Order ID: {order.id}"
        )

        pdf.drawString(
            50,
            730,
            f"Buyer: {order.buyer.username}"
        )

        pdf.drawString(
            50,
            710,
            f"Payment Status: {order.is_paid}"
        )

        pdf.drawString(
            50,
            690,
            f"Order Status: {order.status}"
        )

        y = 650

        pdf.drawString(
            50,
            y,
            "Products:"
        )

        y -= 30

        for item in order.items.all():

            pdf.drawString(
                70,
                y,
                (
                    f"{item.product.name} | "
                    f"Qty: {item.quantity} | "
                    f"Price: ₹{item.price}"
                )
            )

            y -= 25

        pdf.drawString(
            50,
            y - 20,
            (
                f"Total Amount: ₹"
                f"{order.total_amount}"
            )
        )

        pdf.save()

        return response


class TestEmailView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        send_mail(

            subject='Test Email',

            message='Email system is working correctly.',

            from_email=settings.EMAIL_HOST_USER,

            recipient_list=[request.user.email],

            fail_silently=False,
        )

        return Response({

            'message': 'Test email sent successfully'
        })


class SellerOrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        return Order.objects.filter(
            items__product__seller=self.request.user
        ).distinct()
