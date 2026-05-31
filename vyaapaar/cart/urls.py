from django.urls import path

from .views import (
    cart_view,
    AddToCartView,
    RemoveFromCartView,
    UpdateCartItemView
)

urlpatterns = [

    path(
        '',
        cart_view,
        name='cart'
    ),

    path(
        'add/',
        AddToCartView.as_view(),
        name='add_to_cart'
    ),

    path(
        'remove/<int:pk>/',
        RemoveFromCartView.as_view(),
        name='remove_from_cart'
    ),

    path(
        'update/<int:pk>/',
        UpdateCartItemView.as_view(),
        name='update_cart_item'
    ),
]