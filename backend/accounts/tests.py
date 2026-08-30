from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APITestCase

class AuthenticationTests(TestCase):
    def test_user_password_authentication(self):
        user = get_user_model().objects.create_user(username='admin', password='password')
        self.assertTrue(user.check_password('password'))


class AuthenticationAPITests(APITestCase):
    def setUp(self):
        get_user_model().objects.create_user(username='api-admin', password='password')

    def test_login_and_protected_endpoint(self):
        self.assertEqual(self.client.get('/api/v1/clients/').status_code, 401)
        login_response = self.client.post('/api/v1/auth/login/', {'username': 'api-admin', 'password': 'password'}, format='json')
        self.assertEqual(login_response.status_code, 200)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {login_response.data['access']}")
        self.assertEqual(self.client.get('/api/v1/clients/').status_code, 200)
