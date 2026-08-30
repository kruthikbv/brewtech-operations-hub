from django.db import models
from common.constants import CLIENT_ACTIVE, CLIENT_INACTIVE

class Client(models.Model):
    client_code = models.CharField(max_length=30, unique=True, db_index=True)
    client_name = models.CharField(max_length=200, db_index=True)
    contact_person = models.CharField(max_length=150, blank=True)
    phone_number = models.CharField(max_length=40, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True, db_index=True)
    status = models.CharField(max_length=10, choices=[(CLIENT_ACTIVE, 'Active'), (CLIENT_INACTIVE, 'Inactive')], default=CLIENT_ACTIVE, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        indexes = [models.Index(fields=['client_name', 'status'])]
    def __str__(self): return f'{self.client_code} - {self.client_name}'
