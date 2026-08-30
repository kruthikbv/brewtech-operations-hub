from django.db import transaction
from common.constants import MACHINE_AVAILABLE, MACHINE_DEPLOYED, ASSIGNMENT_ACTIVE, ASSIGNMENT_RETURNED
from common.exceptions import ConflictError
from activity_logs.models import ActivityLog
from .models import Machine, MachineAssignment

@transaction.atomic
def assign_machine(*, machine_id, client, assigned_date, notes='', user=None):
    if client.status != 'ACTIVE': raise ConflictError('Only active clients can receive machines.')
    machine = Machine.objects.select_for_update().get(pk=machine_id)
    if machine.status != MACHINE_AVAILABLE: raise ConflictError('Machine is not available for assignment.')
    assignment = MachineAssignment.objects.create(machine=machine, client=client, assigned_date=assigned_date, notes=notes)
    machine.status = MACHINE_DEPLOYED; machine.save(update_fields=['status', 'updated_at'])
    ActivityLog.objects.create(user=user, action_type='ASSIGN', entity_type='MachineAssignment', entity_id=assignment.id, description=f'Assigned machine {machine.machine_code} to {client.client_code}')
    return assignment

@transaction.atomic
def return_machine(*, assignment, returned_date, notes='', user=None):
    assignment = MachineAssignment.objects.select_for_update().select_related('machine').get(pk=assignment.pk)
    if assignment.assignment_status != ASSIGNMENT_ACTIVE: raise ConflictError('Assignment has already been returned.')
    assignment.assignment_status = ASSIGNMENT_RETURNED; assignment.returned_date = returned_date
    if notes: assignment.notes = notes
    assignment.save()
    machine = Machine.objects.select_for_update().get(pk=assignment.machine_id); machine.status = MACHINE_AVAILABLE; machine.save(update_fields=['status', 'updated_at'])
    ActivityLog.objects.create(user=user, action_type='RETURN', entity_type='MachineAssignment', entity_id=assignment.id, description=f'Returned machine {machine.machine_code}')
    return assignment
