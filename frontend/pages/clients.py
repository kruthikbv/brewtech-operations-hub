from api_client.clients_client import ClientsClient
def list_clients(token, **filters): return ClientsClient(token).list(**filters)
