from django.db import models
from common.constants import MACHINE_AVAILABLE, MACHINE_DEPLOYED, MACHINE_UNDER_SERVICE, MACHINE_INACTIVE, ASSIGNMENT_ACTIVE, ASSIGNMENT_RETURNED
from clients.models import Client

class Machine(models.Model):
    machine_code = models.CharField(max_length=30, unique=True, db_index=True)
    machine_model = models.CharField(max_length=150, db_index=True)
    serial_number = models.CharField(max_length=100, unique=True, db_index=True)
    purchase_date = models.DateField()
    status = models.CharField(max_length=20, choices=[(x, x.replace('_', ' ').title()) for x in [MACHINE_AVAILABLE, MACHINE_DEPLOYED, MACHINE_UNDER_SERVICE, MACHINE_INACTIVE]], default=MACHINE_AVAILABLE, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self): return f'{self.machine_code} - {self.machine_model}'

class MachineAssignment(models.Model):
    machine = models.ForeignKey(Machine, on_delete=models.PROTECT, related_name='assignments')
    client = models.ForeignKey(Client, on_delete=models.PROTECT, related_name='machine_assignments')
    assigned_date = models.DateField()
    returned_date = models.DateField(null=True, blank=True)
    assignment_status = models.CharField(max_length=10, choices=[(ASSIGNMENT_ACTIVE, 'Active'), (ASSIGNMENT_RETURNED, 'Returned')], default=ASSIGNMENT_ACTIVE, db_index=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        constraints = [models.UniqueConstraint(fields=['machine'], condition=models.Q(assignment_status=ASSIGNMENT_ACTIVE), name='one_active_assignment_per_machine')]
        indexes = [models.Index(fields=['client', 'assignment_status'])]
