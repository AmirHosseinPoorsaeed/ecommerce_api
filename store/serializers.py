from django.utils.text import slugify
from decimal import Decimal

from rest_framework import serializers

from .models import Comment, Product, Category


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
