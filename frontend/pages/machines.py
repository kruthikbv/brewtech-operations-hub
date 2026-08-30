from api_client.machines_client import MachinesClient
def list_machines(token, **filters): return MachinesClient(token).list(**filters)
