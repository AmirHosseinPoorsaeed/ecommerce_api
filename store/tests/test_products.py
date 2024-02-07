from rest_framework import status
import pytest

from django.urls import reverse


@pytest.mark.django_db
class TestCreateProduct:
    def test_if_user_is_anonymous_returns_401(self, create_product, category_baker):
        category = category_baker

        response = create_product({
            'title': 'aaaaaa',
            'description': 'a',
            'unit_price': 1,
            'inventory': 1,
            'category': reverse('category-detail', args=[category.id])
        })

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_403(self, authenticate, create_product, category_baker):
        category = category_baker
        authenticate(is_staff=False)

        response = create_product({
            'title': 'aaaaaa',
            'description': 'a',
            'unit_price': 1,
            'inventory': 1,
            'category': reverse('category-detail', args=[category.id])
        })

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_data_is_invalid_returns_400(self, authenticate, create_product, category_baker):
        category = category_baker
        authenticate(is_staff=True)

        response = create_product({
            'title': '',
            'description': 'a',
            'price': 1,
            'inventory': 1,
            'category': reverse('category-detail', args=[category.id])
        })

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['title'] is not None

    def test_if_data_is_valid_returns_201(self, authenticate, create_product, category_baker):
        category = category_baker
        authenticate(is_staff=True)

        response = create_product({
            'title': 'aaaaaa',
            'description': 'a',
            'price': 1,
            'inventory': 1,
            'category': reverse('category-detail', args=[category.id])
        })

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] > 0


@pytest.mark.django_db
class TestRetrieveProduct:
    def test_if_product_exists_returns_200(self, api_client, product_baker):
        product = product_baker

        response = api_client.get(reverse('product-detail', args=[product.id]))

        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == product.id
        assert response.data['title'] == product.title
        assert response.data['slug'] == product.slug

    def test_if_category_not_exists_returns_404(self, api_client):
        response = api_client.get(reverse('product-detail', args=[10 ** 10]))

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestUpdateProduct:
    def test_if_user_is_anonymous_returns_401(self, update_product, product_baker):
        product = product_baker

        response = update_product(product.id, {'title': 'aaaaaa'})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_403(self, update_product, authenticate, product_baker):
        product = product_baker
        authenticate(is_staff=False)

        response = update_product(product.id, {'title': 'aaaaaa'})

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_data_is_invalid_returns_400(self, update_product, authenticate, product_baker):
        product = product_baker
        authenticate(is_staff=True)

        response = update_product(product.id, {'title': ''})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['title'] is not None

    def test_if_data_is_valid_returns_201(self, update_product, authenticate, product_baker):
        product = product_baker
        authenticate(is_staff=True)

        response = update_product(product.id, {
            'title': 'aaaaaa',
            'category': reverse('category-detail', args=[product.category.id]),
            'description': product.description,
            'inventory': product.inventory,
            'price': product.unit_price
        })

        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == 'aaaaaa'


@pytest.mark.django_db
class TestDeleteProduct:
    def test_if_user_is_anonymous_returns_401(self, delete_product, product_baker):
        product = product_baker

        response = delete_product(product.id)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_403(self, delete_product, authenticate, product_baker):
        product = product_baker
        authenticate(is_staff=False)

        response = delete_product(product.id)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_user_is_admin_returns_204(self, delete_product, authenticate, product_baker):
        product = product_baker
        authenticate(is_staff=True)

        response = delete_product(product.id)

        assert response.status_code == status.HTTP_204_NO_CONTENT
