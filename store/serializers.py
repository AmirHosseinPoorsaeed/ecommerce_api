from django.utils.text import slugify
from decimal import Decimal

from rest_framework import serializers

from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    price = serializers.DecimalField(
        max_digits=6, decimal_places=2, source='unit_price'
    )
    price_aftre_tax = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'title', 'slug', 'description', 'price',
                  'price_aftre_tax', 'category', 'inventory', ]
        read_only_fields = ['slug', ]

    def get_price_aftre_tax(self, product):
        return round(product.unit_price * Decimal(1.09), 2)

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
