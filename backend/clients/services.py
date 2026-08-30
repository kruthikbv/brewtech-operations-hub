from .models import Client
def create_client(**data): return Client.objects.create(**data)
def update_client(client, **data):
    for key, value in data.items(): setattr(client, key, value)
    client.save(); return client
def deactivate_client(client): client.status = 'INACTIVE'; client.save(update_fields=['status', 'updated_at']); return client
