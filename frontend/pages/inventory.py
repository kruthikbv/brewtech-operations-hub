from api_client.inventory_client import InventoryClient
def list_inventory(token, **filters): return InventoryClient(token).list(**filters)
