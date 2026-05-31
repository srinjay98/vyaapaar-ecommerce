from django.urls import path
from .views import (
    ProductListCreateView,
    ProductDetailView,
    ProductImageUploadView
)


urlpatterns = [

    path(
        '',
        ProductListCreateView.as_view(),
        name='product_list_create'
    ),

    path(
        '<int:pk>/',
        ProductDetailView.as_view(),
        name='product_detail'
    ),

    path(
    'upload-image/',
    ProductImageUploadView.as_view(),
    name='upload_image'
),
]