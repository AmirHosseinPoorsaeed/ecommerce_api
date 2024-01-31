from django.shortcuts import render, get_object_or_404
from django.db.models import Prefetch

from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, RetrieveModelMixin

from .models import Cart, CartItem, Category, Comment, Product
from .serializers import CartSerializer, CategorySerializer, CommentSerializer, ProductSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.prefetch_related(
        'comments'
    ).select_related('category').all()
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


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        product_id = self.kwargs['product_pk']
        return Comment.objects.filter(product_id=product_id)

    def get_serializer_context(self):
        return {
            'product_pk': self.kwargs['product_pk'],
            'user_pk': self.request.user.id
        }


class CartViewSet(CreateModelMixin,
                  RetrieveModelMixin,
                  DestroyModelMixin,
                  GenericViewSet):
    queryset = Cart.objects.prefetch_related(
        Prefetch(
            'items',
            queryset=CartItem.objects.select_related('product').all()
        )
    ).all()
    serializer_class = CartSerializer
