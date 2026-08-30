from api_client.machines_client import MachinesClient
def list_assignments(token): return MachinesClient(token).assignments()
