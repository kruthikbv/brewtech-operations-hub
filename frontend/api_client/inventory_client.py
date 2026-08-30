from .base_client import APIClient
class InventoryClient(APIClient):
    def list(self, **params): return self.get('inventory/', params=params)
    def all_items(self, **params): return self.all('inventory/', **params)
    def create(self, data): return self.post('inventory/', json=data)
    def update(self, inventory_item_id, data): return self.patch(f'inventory/{inventory_item_id}/', json=data)
    def stock_in(self, inventory_item_id, data): return self.post(f'inventory/{inventory_item_id}/stock-in/', json=data)
    def stock_out(self, inventory_item_id, data): return self.post(f'inventory/{inventory_item_id}/stock-out/', json=data)
    def transactions(self, inventory_item_id): return self.get(f'inventory/{inventory_item_id}/transactions/', params={'page_size': 100})
