from .base_client import APIClient
class ClientsClient(APIClient):
    def list(self, **params): return self.get('clients/', params=params)
    def all_clients(self, **params): return self.all('clients/', **params)
    def create(self, data): return self.post('clients/', json=data)
    def update(self, client_id, data): return self.patch(f'clients/{client_id}/', json=data)
    def deactivate(self, client_id): return self.delete(f'clients/{client_id}/')
