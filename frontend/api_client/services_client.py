from .base_client import APIClient
class ServicesClient(APIClient):
    def list(self, **params): return self.get('service-records/', params=params)
    def all_records(self, **params): return self.all('service-records/', **params)
    def create(self, data): return self.post('service-records/', json=data)
    def update(self, service_record_id, data): return self.patch(f'service-records/{service_record_id}/', json=data)
