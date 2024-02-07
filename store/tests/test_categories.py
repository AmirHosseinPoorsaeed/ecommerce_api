from rest_framework import status
import pytest

from django.urls import reverse


@pytest.mark.django_db
class TestCreateCategory:
    def test_if_user_is_anonymous_returns_401(self, create_category):
        response = create_category({'title': 'aaaaaa'})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_403(self, authenticate, create_category):
        authenticate(is_staff=False)

        response = create_category({'title': 'aaaaaa'})

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_data_is_invalid_returns_400(self, authenticate, create_category):
        authenticate(is_staff=True)

        response = create_category({'title': ''})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['title'] is not None

    def test_if_data_is_valid_returns_201(self, authenticate, create_category):
        authenticate(is_staff=True)

        response = create_category({'title': 'aaaaaa'})

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] > 0


@pytest.mark.django_db
class TestRetrieveCategory:
    def test_if_category_exists_returns_200(self, api_client, category_baker):
        category = category_baker

        response = api_client.get(reverse('category-detail', args=[category.id]))

        assert response.status_code == status.HTTP_200_OK
        assert response.data == {
            'id': category.id,
            'title': category.title,
            'description': category.description,
            'number_of_products': 0
        }

    def test_if_category_not_exists_returns_404(self, api_client):
        response = api_client.get(reverse('category-detail', args=[10 ** 10]))

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestUpdateCategory:
    def test_if_user_is_anonymous_returns_401(self, update_category, category_baker):
        category = category_baker

        response = update_category(category.id, {'title': 'aaaaaa'})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_403(self, update_category, authenticate, category_baker):
        category = category_baker
        authenticate(is_staff=False)

        response = update_category(category.id, {'title': 'aaaaaa'})

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_data_is_invalid_returns_400(self, update_category, authenticate, category_baker):
        category = category_baker
        authenticate(is_staff=True)

        response = update_category(category.id, {'title': ''})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['title'] is not None

    def test_if_data_is_valid_returns_201(self, update_category, authenticate, category_baker):
        category = category_baker
        authenticate(is_staff=True)

        response = update_category(category.id, {'title': 'aaaaaa'})

        assert response.status_code == status.HTTP_200_OK
        assert response.data == {
            'id': category.id,
            'title': 'aaaaaa',
            'description': category.description,
            'number_of_products': 0
        }


@pytest.mark.django_db
class TestDeleteCategory:
    def test_if_user_is_anonymous_returns_401(self, delete_category, category_baker):
        category = category_baker

        response = delete_category(category.id)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_403(self, delete_category, authenticate, category_baker):
        category = category_baker
        authenticate(is_staff=False)

        response = delete_category(category.id)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_user_is_admin_returns_204(self, delete_category, authenticate, category_baker):
        category = category_baker
        authenticate(is_staff=True)

        response = delete_category(category.id)

        assert response.status_code == status.HTTP_204_NO_CONTENT
