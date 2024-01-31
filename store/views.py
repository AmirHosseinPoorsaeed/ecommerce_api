from django.shortcuts import render, get_object_or_404

from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status

from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.select_related('category').all()
    serializer_class = ProductSerializer

    def destroy(self, request, pk):
        product = get_object_or_404(
            Product, pk=pk
        )
        if product.order_items.count() > 0:
            return Response(
                {'error': 'There is some order items that include this product.'},
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            )
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.prefetch_related('products').all()
    serializer_class = CategorySerializer

    def destroy(self, request, pk):
        category = get_object_or_404(
            Category, pk=pk
        )
        if category.products.count() > 0:
            return Response(
                {'error': 'There is some products that include this category.'},
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            )
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)