from django.contrib.auth import get_user_model
from django.urls import reverse

from model_bakery import baker
from rest_framework.test import APIClient
import pytest

from store.models import Cart, CartItem, Category, Comment, Customer, Order, OrderItem, Product

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def create_category(api_client):
    def do_create_category(category):
        return api_client.post(reverse('category-list'), category)
    return do_create_category


@pytest.fixture
def update_category(api_client):
    def do_update_category(category_id, category):
        return api_client.put(reverse('category-detail', args=[category_id]), category)
    return do_update_category


@pytest.fixture
def delete_category(api_client):
    def do_delete_category(category_id):
        return api_client.delete(reverse('category-detail', args=[category_id]))
    return do_delete_category


@pytest.fixture
def create_product(api_client):
    def do_create_product(product):
        return api_client.post(reverse('product-list'), product)
    return do_create_product


@pytest.fixture
def update_product(api_client):
    def do_update_product(product_id, product):
        return api_client.put(reverse('product-detail', args=[product_id]), product)
    return do_update_product


@pytest.fixture
def delete_product(api_client):
    def do_delete_product(product_id):
        return api_client.delete(reverse('product-detail', args=[product_id]))
    return do_delete_product


@pytest.fixture
def create_comment(api_client):
    def do_create_comment(product_pk, comment):
        return api_client.post(reverse('product-comments-list', args=[product_pk]), comment)
    return do_create_comment


@pytest.fixture
def update_comment(api_client):
    def do_update_comment(product_pk, comment_id, comment):
        return api_client.put(reverse('product-comments-detail', args=[product_pk, comment_id]), comment)
    return do_update_comment


@pytest.fixture
def delete_comment(api_client):
    def do_delete_comment(product_pk, comment_id):
        return api_client.delete(reverse('product-comments-detail', args=[product_pk, comment_id]))
    return do_delete_comment


@pytest.fixture
def create_cart(api_client):
    def do_create_cart():
        return api_client.post(reverse('cart-list'))
    return do_create_cart


@pytest.fixture
def delete_cart(api_client):
    def do_delete_cart(cart_id):
        return api_client.delete(reverse('cart-detail', args=[cart_id]))
    return do_delete_cart


@pytest.fixture
def create_order(api_client):
    def do_create_order(order):
        return api_client.post(reverse('order-list'), order)
    return do_create_order


@pytest.fixture
def update_order(api_client):
    def do_update_order(order_id, order):
        return api_client.patch(reverse('order-detail', args=[order_id]), order)
    return do_update_order


@pytest.fixture
def delete_order(api_client):
    def do_delete_order(order_id):
        return api_client.delete(reverse('order-detail', args=[order_id]))
    return do_delete_order


@pytest.fixture
def category_baker():
    return baker.make(Category)


@pytest.fixture
def product_baker():
    return baker.make(Product)


@pytest.fixture
def cart_baker():
    return baker.make(Cart)


@pytest.fixture
def cart_item_baker(cart_baker):
    cart = cart_baker
    return baker.make(CartItem, cart=cart)


@pytest.fixture
def order_baker():
    def do_order_baker(user):
        customer = Customer.objects.get(user=user)
        return baker.make(Order, customer=customer)
    return do_order_baker


@pytest.fixture
def order_item_baker(order_baker):
    def do_order_item_baker(user):
        order = order_baker(user)
        return baker.make(OrderItem, order=order)
    return do_order_item_baker


@pytest.fixture
def comment_baker(product_baker):
    product = product_baker
    return baker.make(Comment, product=product)


@pytest.fixture
def authenticate(api_client):
    def do_authenticate(is_staff=False):
        user = User.objects.create_user(
            username='testuser', password='testpass', is_staff=is_staff)
        api_client.force_authenticate(user=user)
        return user
    return do_authenticate



