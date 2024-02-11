from rest_framework import status
from django.contrib.auth import get_user_model
import pytest

from django.urls import reverse


@pytest.mark.django_db
class TestCreateOrder:
    def test_if_user_is_anonymous_returns_401(self, create_order):
        response = create_order({'cart_id': 'a'})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_and_data_is_invalid_returns_400(self, create_order, authenticate):
        authenticate(is_staff=False)

        response = create_order({'cart_id': 'a'})

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_user_is_not_admin_and_data_is_valid_but_cart_is_empty_returns_400(self, create_order, authenticate, cart_baker):
        cart = cart_baker
        authenticate(is_staff=False)

        response = create_order({'cart_id': cart.id})

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_user_is_not_admin_and_data_is_valid_and_cart_is_not_empty_returns_200(self, create_order, authenticate, cart_item_baker):
        cart_item = cart_item_baker
        authenticate(is_staff=False)

        response = create_order({'cart_id': cart_item.cart.id})

        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] > 0

    def test_if_user_is_admin_and_data_is_invalid_returns_400(self, create_order, authenticate):
        authenticate(is_staff=True)

        response = create_order({'cart_id': 'a'})

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_user_is_admin_and_data_is_valid_but_cart_is_empty_returns_400(self, create_order, authenticate, cart_baker):
        cart = cart_baker
        authenticate(is_staff=True)

        response = create_order({'cart_id': cart.id})

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_user_is_admin_and_data_is_valid_and_cart_is_not_empty_returns_200(self, create_order, authenticate, cart_item_baker):
        cart_item = cart_item_baker
        authenticate(is_staff=True)

        response = create_order({'cart_id': cart_item.cart.id})

        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] > 0


@pytest.mark.django_db
class TestRetrieveOrder:
    def test_if_user_is_anonymous_returns_401(self, api_client):
        response = api_client.get(reverse('order-detail', args=['a']))

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_if_user_is_not_admin_returns_200(self, authenticate, api_client, order_item_baker):
        user = authenticate(is_staff=False)
        order_item = order_item_baker(user)

        response = api_client.get(reverse('order-detail', args=[order_item.order.id]))

        assert response.status_code == status.HTTP_200_OK
    
    def test_if_user_is_admin_returns_200(self, authenticate, api_client, order_item_baker):
        user = authenticate(is_staff=True)
        order_item = order_item_baker(user)

        response = api_client.get(reverse('order-detail', args=[order_item.order.id]))

        assert response.status_code == status.HTTP_200_OK
    
    def test_if_order_not_exists_returns_404(self, authenticate, api_client):
        authenticate(is_staff=True)

        response = api_client.get(reverse('order-detail', args=[10 * 10]))

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestUpdateOrder:
    def test_if_user_is_anonymous_returns_401(self, update_order):
        response = update_order(1, {})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_and_data_is_invalid_returns_403(self, authenticate, order_item_baker, update_order):
        user = authenticate(is_staff=False)
        order_item = order_item_baker(user)

        response = update_order(order_item.order.id, {'status': ''})

        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_if_user_is_not_admin_and_data_is_valid_returns_403(self, authenticate, order_item_baker, update_order):
        user = authenticate(is_staff=False)
        order_item = order_item_baker(user)

        response = update_order(order_item.order.id, {'status': 'p'})

        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_if_user_is_admin_and_data_is_invalid_returns_400(self, authenticate, order_item_baker, update_order):
        user = authenticate(is_staff=True)
        order_item = order_item_baker(user)

        response = update_order(order_item.order.id, {'status': 'a'})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_if_user_is_admin_and_data_is_valid_returns_200(self, authenticate, order_item_baker, update_order):
        user = authenticate(is_staff=True)
        order_item = order_item_baker(user)

        response = update_order(order_item.order.id, {'status': 'p'})

        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestDeleteOrder:
    def test_if_user_is_anonymous_returns_401(self, delete_order):
        response = delete_order(1)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_if_user_is_not_admin_returns_403(self, authenticate, order_item_baker, delete_order):
        user = authenticate(is_staff=False)
        order_item = order_item_baker(user)

        response = delete_order(order_item.order.id)

        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_if_user_is_admin_and_order_has_order_item_returns_405(self, authenticate, order_item_baker, delete_order):
        user = authenticate(is_staff=True)
        order_item = order_item_baker(user)

        response = delete_order(order_item.order.id)

        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
