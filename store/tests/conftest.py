from django.contrib.auth import get_user_model
from django.urls import reverse

from model_bakery import baker
from rest_framework.test import APIClient
import pytest

from store.models import Category, Product

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
def category_baker():
    return baker.make(Category)


@pytest.fixture
def product_baker():
    return baker.make(Product)


@pytest.fixture
def authenticate(api_client):
    def do_authenticate(is_staff=False):
        return api_client.force_authenticate(user=User(is_staff=is_staff))
    return do_authenticate
