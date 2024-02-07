from rest_framework import status
import pytest

from django.urls import reverse


@pytest.mark.django_db
class TestCreateComment:
    def test_if_user_is_anonymous_returns_401(self, create_comment, product_baker):
        product = product_baker

        response = create_comment(product.id, {
            'body': 'a'
        })

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_and_data_is_invalid_returns_400(self, authenticate, create_comment, product_baker):
        product = product_baker
        authenticate(is_staff=False)

        response = create_comment(product.id, {
            'body': ''
        })

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['body'] is not None

    def test_if_user_is_admin_and_data_is_invalid_returns_400(self, authenticate, create_comment, product_baker):
        product = product_baker
        authenticate(is_staff=True)

        response = create_comment(product.id, {
            'body': ''
        })

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['body'] is not None

    def test_if_user_is_not_admin_and_data_is_valid_returns_201(self, authenticate, create_comment, product_baker):
        product = product_baker
        authenticate(is_staff=False)

        response = create_comment(product.id, {
            'body': 'a',
        })

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] > 0

    def test_if_user_is_admin_and_data_is_valid_returns_201(self, authenticate, create_comment, product_baker):
        product = product_baker
        authenticate(is_staff=True)

        response = create_comment(product.id, {
            'body': 'a'
        })

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] > 0


@pytest.mark.django_db
class TestRetrieveComment:
    def test_if_comment_exists_returns_200(self, api_client, comment_baker):
        comment = comment_baker

        response = api_client.get(reverse('product-comments-detail', args=[comment.product.id, comment.id]))

        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == comment.id
        assert response.data['body'] == comment.body
        assert response.data['status'] == comment.status

    def test_if_comment_not_exists_returns_404(self, api_client):
        response = api_client.get(reverse('product-comments-detail', args=[10 ** 10, 10 ** 10]))

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestUpdateComment:
    def test_if_user_is_anonymous_returns_401(self, update_comment, comment_baker):
        comment = comment_baker

        response = update_comment(comment.product.id, comment.id, {
            'body': 'a'
        })

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_and_data_is_invalid_returns_400(self, update_comment, authenticate, comment_baker):
        comment = comment_baker
        authenticate(is_staff=False)

        response = update_comment(comment.product.id, comment.id, {
            'body': ''
        })

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['body'] is not None
    
    def test_if_user_is_admin_and_data_is_invalid_returns_400(self, update_comment, authenticate, comment_baker):
        comment = comment_baker
        authenticate(is_staff=True)

        response = update_comment(comment.product.id, comment.id, {
            'body': ''
        })

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['body'] is not None

    def test_if_user_is_not_admin_and_data_is_valid_returns_201(self, authenticate, update_comment, comment_baker):
        comment = comment_baker
        authenticate(is_staff=False)

        response = update_comment(comment.product.id, comment.id, {
            'body': 'a',
        })

        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] > 0
    
    def test_if_user_is_not_admin_and_data_is_valid_returns_201(self, authenticate, update_comment, comment_baker):
        comment = comment_baker
        authenticate(is_staff=True)

        response = update_comment(comment.product.id, comment.id, {
            'body': 'a',
        })

        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] > 0


@pytest.mark.django_db
class TestDeleteComment:
    def test_if_user_is_anonymous_returns_401(self, delete_comment, comment_baker):
        comment = comment_baker

        response = delete_comment(comment.product.id, comment.id)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_204(self, delete_comment, authenticate, comment_baker):
        comment = comment_baker
        authenticate(is_staff=False)

        response = delete_comment(comment.product.id, comment.id)

        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_if_user_is_admin_returns_204(self, delete_comment, authenticate, comment_baker):
        comment = comment_baker
        authenticate(is_staff=True)

        response = delete_comment(comment.product.id, comment.id)

        assert response.status_code == status.HTTP_204_NO_CONTENT
