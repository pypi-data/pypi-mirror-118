from django.urls import reverse
from django.conf import settings
from rest_framework import status
from rest_framework.test import APITestCase
from djrest_wrapper.exceptions.apis import errors
from ..models.user_models import User


class UserViewSetTestCase(APITestCase):
    def setUp(self):
        pass

    def test_create_user_view(self):
        url = reverse('user-list')
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'test'
        }
        response = self.client.post(path=url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json().get('err'), False)
        self.assertEqual(response.json().get(
            'err_code'), errors.ERR_SUCCESSFUL)
        self.assertIsNotNone(response.json().get(
            'data').get('user').get('access_token'))

    def test_signin_user_view(self):
        self.test_create_user_view()
        url = reverse('user-signin')
        data = {
            'username': 'testuser',
            'password': 'test'
        }
        response = self.client.post(path=url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('err'), False)
        self.assertEqual(response.json().get(
            'err_code'), errors.ERR_SUCCESSFUL)
        self.assertIsNotNone(response.json().get(
            'data').get('user').get('access_token'))
        return response.json().get('data').get('user')

    def test_retrieve_user_profile_view_succesful(self):
        user = self.test_signin_user_view()
        self.client.credentials(
            HTTP_AUTHORIZATION=f'{settings.SHA_ACCOUNTS.get("JWT_AUTH_RAELM")} {user.get("access_token")}')
        url = reverse('user-detail', args={user.get('id')})
        response = self.client.get(path=url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('err'), False)
        self.assertEqual(response.json().get(
            'err_code'), errors.ERR_SUCCESSFUL)
        self.assertIsNotNone(response.json().get('data').get('user'))

    def test_retrieve_user_profile_view_failed(self):
        user = self.test_signin_user_view()
        url = reverse('user-detail', args={user.get('id')})
        response = self.client.get(path=url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json().get('err'), True)
        self.assertEqual(response.json().get(
            'err_code'), errors.ERR_PERMISSION_DENIED)

    def test_retrieve_user_profile_admin_view(self):
        superuser = User.objects.create_superuser(
            username='superuser', email='superuser@example.com', password='superuser')
        user = User.objects.create(
            username='testuser', email='testuser@example.com', password='testuser')
        url = reverse('user-signin')
        data = {
            'username': superuser.username,
            'password': 'superuser'
        }
        response = self.client.post(path=url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('err'), False)
        self.assertEqual(response.json().get(
            'err_code'), errors.ERR_SUCCESSFUL)
        self.assertIsNotNone(response.json().get(
            'data').get('user').get('access_token'))
        self.client.credentials(
            HTTP_AUTHORIZATION=f'{settings.SHA_ACCOUNTS.get("JWT_AUTH_RAELM")} {response.json().get("data").get("user").get("access_token")}')
        url = reverse('user-detail', args={user.id})
        response = self.client.get(path=url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('err'), False)
        self.assertEqual(response.json().get(
            'err_code'), errors.ERR_SUCCESSFUL)
        self.assertIsNotNone(response.json().get('data').get('user'))
