from django.shortcuts import render

# Create your views here.
from rest_framework import generics, status

from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated

from .models import Cart, CartItem

from .serializers import (
    CartSerializer,
    CartItemSerializer
)

from products.models import Product


# class CartView(generics.RetrieveAPIView):

#     serializer_class = CartSerializer

#     permission_classes = [IsAuthenticated]

#     def get_object(self):

#         cart, created = Cart.objects.get_or_create(
#             user=self.request.user
#         )

#         return cart

# def cart_view(request):

#     token = request.session.get('access')

#     headers = {

#         'Authorization': f'Bearer {token}'
#     }

#     response = requests.get(

#         'http://web:8000/api/cart/',

#         headers=headers
#     )

#     cart_data = response.json()

#     total_price = 0

#     for item in cart_data.get('items', []):

#         item['subtotal'] = (

#             float(item['product']['price']) *
#             item['quantity']
#         )

#         total_price += item['subtotal']

#     context = {

#         'cart': cart_data,

#         'total_price': total_price
#     }

#     return render(
#         request,
#         'cart.html',
#         context
#     )

def cart_view(request):

    if not request.user.is_authenticated:

        return redirect('login')

    cart = get_object_or_404(
        Cart,
        user=request.user
    )

    cart_items = cart.items.all()

    total_price = 0

    for item in cart_items:

        item.subtotal = (
            item.product.price * item.quantity
        )

        total_price += item.subtotal

    context = {

        'cart_items': cart_items,

        'total_price': total_price
    }

    return render(
        request,
        'cart.html',
        context
    )


class AddToCartView(generics.CreateAPIView):

    serializer_class = CartItemSerializer

    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):

        cart, created = Cart.objects.get_or_create(
            user=request.user
        )

        product_id = request.data.get('product')

        quantity = int(
            request.data.get('quantity', 1)
        )

        product = Product.objects.get(id=product_id)

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product
        )

        if not created:

            cart_item.quantity += quantity

        else:

            cart_item.quantity = quantity

        cart_item.save()

        serializer = self.get_serializer(cart_item)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )
class RemoveFromCartView(generics.DestroyAPIView):

    queryset = CartItem.objects.all()

    serializer_class = CartItemSerializer

    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        return CartItem.objects.filter(
            cart__user=self.request.user
        ) 

class UpdateCartItemView(generics.UpdateAPIView):

    serializer_class = CartItemSerializer

    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        return CartItem.objects.filter(
            cart__user=self.request.user
        )

    def patch(self, request, *args, **kwargs):

        cart_item = self.get_object()

        quantity = request.data.get('quantity')

        if quantity is not None:

            cart_item.quantity = quantity

            cart_item.save()

        serializer = self.get_serializer(cart_item)

        return Response(serializer.data)       