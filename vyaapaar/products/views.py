from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from rest_framework.permissions import ( 
IsAuthenticated,    
IsAuthenticatedOrReadOnly
)

from .models import Product
from .serializers import ProductSerializer
from .permissions import (
    IsSeller,
    IsSellerOrReadOnly
)

from rest_framework.parsers import MultiPartParser, FormParser
from .models import ProductImage
from .serializers import ProductImageUploadSerializer


class ProductListCreateView(generics.ListCreateAPIView):

    queryset = Product.objects.all()

    serializer_class = ProductSerializer

    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):

        if self.request.user.role != 'seller':
            raise PermissionError(
                'Only sellers can create products'
            )

        serializer.save(
            seller=self.request.user
        )


class ProductDetailView(
    generics.RetrieveUpdateDestroyAPIView
):

    queryset = Product.objects.all()

    serializer_class = ProductSerializer

    permission_classes = [IsSellerOrReadOnly]

class ProductImageUploadView(generics.CreateAPIView):

    queryset = ProductImage.objects.all()

    serializer_class = ProductImageUploadSerializer

    permission_classes = [IsAuthenticated]

    parser_classes = [MultiPartParser, FormParser]

    def perform_create(self, serializer):

        product = serializer.validated_data['product']

        if product.seller != self.request.user:
            raise PermissionError(
                'You can upload images only for your own products'
            )

        serializer.save()    