from django.utils.text import slugify
from decimal import Decimal

from rest_framework import serializers

from .models import Cart, CartItem, Comment, Product, Category


class CategorySerializer(serializers.ModelSerializer):
    number_of_products = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'title', 'description', 'number_of_products', ]

    def validate(self, data):
        if len(data['title']) < 6:
            raise serializers.ValidationError(
                'Category title should be at least 6.')
        return data

    def get_number_of_products(self, category):
        return category.products.count()


class ProductSerializer(serializers.ModelSerializer):
    price = serializers.DecimalField(
        max_digits=6, decimal_places=2, source='unit_price'
    )
    price_aftre_tax = serializers.SerializerMethodField()
    category = serializers.HyperlinkedRelatedField(
        view_name='category-detail',
        queryset=Category.objects.all()
    )
    number_of_comments = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'title', 'slug', 'description', 'price',
                  'price_aftre_tax', 'category', 'inventory', 'number_of_comments', ]
        read_only_fields = ['slug', ]

    def get_price_aftre_tax(self, product):
        return round(product.unit_price * Decimal(1.09), 2)

    def get_number_of_comments(self, product):
        return product.comments.count()

    def validate(self, data):
        if len(data['title']) < 6:
            raise serializers.ValidationError(
                'Product title should be at least 6.')
        return data

    def create(self, validated_data):
        product = Product(**validated_data)
        product.slug = slugify(product.title)
        product.save()
        return product


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'author', 'body', 'status', ]
        read_only_fields = ['author', ]

    def create(self, validated_data):
        product_id = self.context['product_pk']
        user_id = self.context['user_pk']
        return Comment.objects.create(
            product_id=product_id,
            author_id=user_id,
            **validated_data
        )


class CartItemProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'unit_price', ]


class CartItemSerializer(serializers.ModelSerializer):
    product = CartItemProductSerializer()
    item_total = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'item_total', ]

    def get_item_total(self, cart_item):
        return cart_item.quantity * cart_item.product.unit_price


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'items', 'datetime_created', 'total_price', ]
        read_only_fields = ['id', ]

    def get_total_price(self, cart):
        return sum(
            item.quantity * item.product.unit_price 
            for item in cart.items.all()
        )


class AddCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', ]

    def create(self, validated_data):
        product = validated_data.get('product')
        quantity = validated_data.get('quantity')
        cart_id = self.context['cart_pk']
        
        try:
            cart_item = CartItem.objects.get(cart_id=cart_id, product_id=product.id)
            cart_item.quantity += quantity
            cart_item.save()
        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(cart_id=cart_id, **validated_data)
        
        return cart_item


class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['quantity', ]
