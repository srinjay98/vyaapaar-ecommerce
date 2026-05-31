from django.urls import path

from .views import (
    PlaceOrderView,
    OrderListView,
    SellerOrderListView,
    CreatePaymentView,
    VerifyPaymentView,
    GenerateInvoiceView,
    TestEmailView
)

urlpatterns = [

    path(
        'place/',
        PlaceOrderView.as_view(),
        name='place_order'
    ),

    path(
        '',
        OrderListView.as_view(),
        name='order_list'
    ),
    
    path(
         'seller/',
          SellerOrderListView.as_view(),
          name='seller_orders'
    ),

    # path(
    #      'payment/<int:order_id>/',
    #       CreatePaymentView.as_view(),
    #       name='create_payment'
    # ),

    path(
         'create-payment/<int:order_id>/',
         CreatePaymentView.as_view(),
         name='create_payment'
         ),

    path(
         'verify-payment/',
          VerifyPaymentView.as_view(),
          name='verify_payment'
        ),

    path(
        'invoice/<int:order_id>/',
         GenerateInvoiceView.as_view(),
         name='generate_invoice'
        ), 

    path(
        'test-email/',
         TestEmailView.as_view(),
         name='test_email'
        ),
    
]