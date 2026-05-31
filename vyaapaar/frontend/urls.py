from django.urls import path

from .views import (
    home,
    product_detail,
    add_to_cart,
    cart_view,
    register_view,
    login_view,
    logout_view,
    checkout_view,
    orders_view,
    increase_quantity,
    decrease_quantity,
    remove_cart_item,
    seller_dashboard,
    add_product,
    edit_product,
    delete_product,
    payment_view,
    add_review,
    wishlist_view,
    add_to_wishlist,
    remove_from_wishlist,
    seller_orders_view,
    update_order_status,
    apply_coupon_view
)

from .forms import (ProductForm, ProductImageForm)

urlpatterns = [

    path('', home, name='home'),

    path(
        'product/<int:product_id>/',
        product_detail,
        name='product_detail'
    ),

    path(
        'add-to-cart/<int:product_id>/',
        add_to_cart,
        name='add_to_cart'
    ),

    path(
        'cart/',
        cart_view,
        name='cart_view'
    ),

    path(
        'register/',
        register_view,
        name='register'
    ),

    path(
        'login/',
        login_view,
        name='login'
    ),

    path(
        'logout/',
        logout_view,
        name='logout'
    ),

    path(
        'checkout/',
        checkout_view,
        name='checkout'
    ),

    path(
        'orders/',
        orders_view,
        name='orders_view'
    ),

    path(
        'increase/<int:item_id>/',
        increase_quantity,
        name='increase_quantity'
        ),

    path(
        'decrease/<int:item_id>/',
        decrease_quantity,
        name='decrease_quantity'
    ),

    path(
        'remove/<int:item_id>/',
        remove_cart_item,
        name='remove_cart_item'
    ),

    path(
       'seller/dashboard/',
        seller_dashboard,
        name='seller_dashboard'
       ),

    path(
        'seller/add-product/',
        add_product,
        name='add_product'
    ),   

    path(
        'seller/edit-product/<int:product_id>/',
        edit_product,
        name='edit_product'
    ),

    path(
        'seller/delete-product/<int:product_id>/',
        delete_product,
        name='delete_product'
    ),

    path(
        'payment/<int:order_id>/',
        payment_view,
        name='payment_view'
    ),
    
    path(
       'add-review/<int:product_id>/',
        add_review,
        name='add_review'
    ),

    path(
        'wishlist/',
        wishlist_view,
        name='wishlist_view'
    ),

    path(
        'add-to-wishlist/<int:product_id>/',
        add_to_wishlist,
        name='add_to_wishlist'
    ),

    path(
        'remove-wishlist/<int:wishlist_id>/',
         remove_from_wishlist,
         name='remove_from_wishlist'
        ),

    path(
        'seller-orders/',
         seller_orders_view,
         name='seller_orders_view'
        ),

    path(
        'seller/update-order/<int:order_id>/',
        update_order_status,
        name='update_order_status'
        ),

    path(
        'apply-coupon/',
        apply_coupon_view,
        name='apply_coupon'
        ),        
]
