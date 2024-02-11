from django.shortcuts import render, get_object_or_404
from django.db.models import Prefetch

from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, RetrieveModelMixin
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser, IsAuthenticated

from django_filters.rest_framework import DjangoFilterBackend

from .filters import ProductFilter
from .paginations import CustomPagination
from .permissions import IsAdminOrReadOnly
from .models import \
    Cart, \
    CartItem, \
    Category, \
    Comment, \
    Customer, \
    Order, \
    OrderItem, \
    Product, \
    ProductImage
from .serializers import \
    AddCartItemSerializer, \
    CartItemSerializer, \
    CartSerializer, \
    CategorySerializer, \
    CommentSerializer, \
    CustomerSerializer, \
    OrderCreateSerializer, \
    OrderForAdminSerializer, \
    OrderSerializer, \
    ProductImageSerializer, \
    ProductSerializer, \
    UpdateCartItemSerializer, \
    UpdateOrderSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.prefetch_related(
        'comments',
        'images'
    ).select_related('category').all()
    serializer_class = ProductSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['title', 'category__title', ]
    ordering_fields = ['unit_price', 'inventory', ]
    permission_classes = [IsAdminOrReadOnly]

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
    

class ProductImageViewSet(ModelViewSet):
    serializer_class = ProductImageSerializer
    permission_classes = [IsAdminOrReadOnly]
    
    def get_queryset(self):
        product_id = self.kwargs['product_pk']
        return ProductImage.objects.filter(product_id=product_id)
    
    def get_serializer_context(self):
        return {'product_pk': self.kwargs['product_pk']}
    


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.prefetch_related('products').all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]

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
    permission_classes = [IsAuthenticatedOrReadOnly]

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

    def get_permissions(self):
        if self.request.method in ['PATCH', 'DELETE']:
            return [IsAdminUser()]
        return [IsAuthenticated()]

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
    
    def destroy(self, request, pk):
        order = get_object_or_404(
            Order,
            pk=pk
        )
        if order.items.count() > 0:
            return Response({
                'error': 'The order has some order items'}, 
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            )
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAdminUser]

    @action(detail=False, methods=['GET', 'PUT'], permission_classes=[IsAuthenticated])
    def me(self, request):
        user_id = request.user.id
        customer = Customer.objects.get(user_id=user_id)
        if request.method == 'GET':
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = CustomerSerializer(customer, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)