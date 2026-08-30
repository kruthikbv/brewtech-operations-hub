from api_client.services_client import ServicesClient
def list_services(token, **filters): return ServicesClient(token).list(**filters)
