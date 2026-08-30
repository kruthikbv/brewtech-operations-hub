from django.db import models
from machines.models import Machine
from common.constants import SERVICE_SCHEDULED, SERVICE_IN_PROGRESS, SERVICE_COMPLETED, SERVICE_CANCELLED

class ServiceRecord(models.Model):
    machine = models.ForeignKey(Machine, on_delete=models.PROTECT, related_name='service_records')
    service_date = models.DateField()
    service_type = models.CharField(max_length=30, choices=[(x, x.replace('_', ' ').title()) for x in ['ROUTINE_SERVICE', 'CLEANING', 'REPAIR', 'INSPECTION']])
    technician_name = models.CharField(max_length=150)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=[(x, x.replace('_', ' ').title()) for x in [SERVICE_SCHEDULED, SERVICE_IN_PROGRESS, SERVICE_COMPLETED, SERVICE_CANCELLED]], default=SERVICE_SCHEDULED, db_index=True)
    previous_machine_status = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
