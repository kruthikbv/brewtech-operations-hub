from .base_client import APIClient
class MachinesClient(APIClient):
    def list(self, **params): return self.get('machines/', params=params)
    def all_machines(self, **params): return self.all('machines/', **params)
    def create(self, data): return self.post('machines/', json=data)
    def update(self, machine_id, data): return self.patch(f'machines/{machine_id}/', json=data)
    def assignments(self, **params): return self.get('assignments/', params=params)
    def all_assignments(self, **params): return self.all('assignments/', **params)
    def assign(self, data): return self.post('assignments/', json=data)
    def return_machine(self, assignment_id, data): return self.post(f'assignments/{assignment_id}/return/', json=data)
