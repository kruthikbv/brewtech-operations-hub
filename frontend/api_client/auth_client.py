from .base_client import APIClient
class AuthClient(APIClient):
    def login(self, username, password): return self.post('auth/login/', json={'username': username, 'password': password})
    def me(self): return self.get('auth/me/')
