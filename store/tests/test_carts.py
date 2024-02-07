from rest_framework import status
import pytest

from django.urls import reverse


@pytest.mark.django_db
class TestCreateComment:
    def test_if_user_is_anonymous_returns_201(self, create_cart):
        response = create_cart()

        assert response.status_code == status.HTTP_201_CREATED
        assert 'id' in response.data
    
    def test_if_user_is_not_admin_returns_201(self, authenticate, create_cart):
        authenticate(is_staff=False)

        response = create_cart()

        assert response.status_code == status.HTTP_201_CREATED
        assert 'id' in response.data
    
    def test_if_user_is_admin_returns_201(self, authenticate, create_cart):
        authenticate(is_staff=True)

        response = create_cart()

        assert response.status_code == status.HTTP_201_CREATED
        assert 'id' in response.data


@pytest.mark.django_db
class TestRetrieveCart:
    def test_if_cart_exists_returns_200(self, api_client, cart_baker):
        cart = cart_baker

        response = api_client.get(reverse('cart-detail', args=[cart.id]))

        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == str(cart.id)

    def test_if_cart_not_exists_returns_404(self, api_client):
        response = api_client.get(reverse('cart-detail', args=[10 ** 10]))

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestDeleteCart:
    def test_if_user_is_anonymous_returns_204(self, delete_cart, cart_baker):
        cart = cart_baker

        response = delete_cart(cart.id)

        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_if_user_is_not_admin_returns_204(self, delete_cart, authenticate, cart_baker):
        cart = cart_baker
        authenticate(is_staff=False)

        response = delete_cart(cart.id)

        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_if_user_is_admin_returns_204(self, delete_cart, authenticate, cart_baker):
        cart = cart_baker
        authenticate(is_staff=True)

        response = delete_cart(cart.id)

        assert response.status_code == status.HTTP_204_NO_CONTENT
