from django.shortcuts import render, get_object_or_404
from django.db.models import Prefetch

from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, RetrieveModelMixin

from .models import Cart, CartItem, Category, Comment, Order, OrderItem, Product
from .serializers import \
    AddCartItemSerializer, \
    CartItemSerializer, \
    CartSerializer, \
    CategorySerializer, \
    CommentSerializer, \
    OrderCreateSerializer, \
    OrderForAdminSerializer, \
    OrderSerializer, \
    ProductSerializer, \
    UpdateCartItemSerializer, \
    UpdateOrderSerializer


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


class CartItemViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete', ]

    def get_queryset(self):
        cart_id = self.kwargs['cart_pk']
        return CartItem.objects.select_related('product').filter(cart_id=cart_id)

    def get_serializer_context(self):
        return {'cart_pk': self.kwargs['cart_pk']}

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer
        elif self.request.method == 'PATCH':
            return UpdateCartItemSerializer
        return CartItemSerializer


class OrderViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete', 'options', 'head', ]

    def get_queryset(self):
        user = self.request.user
        queryset = Order.objects.prefetch_related(
            Prefetch(
                'items',
                queryset=OrderItem.objects.select_related('product').all()
            )
        ).select_related('customer__user').all()

        if user.is_staff:
            return queryset

        return queryset.filter(customer__user_id=user.id)

    def get_serializer_class(self):
        user = self.request.user
        if self.request.method == 'POST':
            return OrderCreateSerializer
        elif self.request.method == 'PATCH':
            return UpdateOrderSerializer

        if user.is_staff:
            return OrderForAdminSerializer
        return OrderSerializer

    def get_serializer_context(self):
        return {
            'user_pk': self.request.user.id
        }

    def create(self, request):
        create_order_serializer = OrderCreateSerializer(
            data=request.data,
            context={'user_pk': self.request.user.id}
        )
        create_order_serializer.is_valid(raise_exception=True)
        order = create_order_serializer.save()
        serializer = OrderSerializer(order)
        return Response(serializer.data)
