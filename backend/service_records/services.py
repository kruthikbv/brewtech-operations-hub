from django.db import transaction
from activity_logs.models import ActivityLog
from common.constants import SERVICE_IN_PROGRESS, SERVICE_COMPLETED, SERVICE_CANCELLED, MACHINE_UNDER_SERVICE
from common.exceptions import ConflictError
from machines.models import Machine
from .models import ServiceRecord


FINAL_STATUSES = {SERVICE_COMPLETED, SERVICE_CANCELLED}


def _start_service(record, machine):
    if machine.status == MACHINE_UNDER_SERVICE:
        raise ConflictError('Machine is already under service.')
    record.previous_machine_status = machine.status
    machine.status = MACHINE_UNDER_SERVICE
    machine.save(update_fields=['status', 'updated_at'])


def _finish_service(record, machine):
    if record.previous_machine_status and machine.status == MACHINE_UNDER_SERVICE:
        machine.status = record.previous_machine_status
        machine.save(update_fields=['status', 'updated_at'])

@transaction.atomic
def create_service_record(*, data, user=None):
    machine = Machine.objects.select_for_update().get(pk=data['machine'].pk)
    data['machine'] = machine
    record = ServiceRecord(**data)
    if record.status == SERVICE_IN_PROGRESS:
        _start_service(record, machine)
    record.save()
    ActivityLog.objects.create(user=user, action_type='SERVICE_CREATE', entity_type='ServiceRecord', entity_id=record.id, description=f'Created service record for {record.machine.machine_code}')
    return record

@transaction.atomic
def update_service_record(*, record, data, user=None):
    record = ServiceRecord.objects.select_for_update().select_related('machine').get(pk=record.pk)
    machine = Machine.objects.select_for_update().get(pk=record.machine_id)
    old_status = record.status
    new_status = data.get('status', old_status)
    if old_status in FINAL_STATUSES and new_status != old_status:
        raise ConflictError('Completed or cancelled service records cannot be reopened.')
    for key, value in data.items(): setattr(record, key, value)
    if old_status != SERVICE_IN_PROGRESS and new_status == SERVICE_IN_PROGRESS:
        _start_service(record, machine)
    elif old_status == SERVICE_IN_PROGRESS and new_status in FINAL_STATUSES:
        _finish_service(record, machine)
    record.save(); ActivityLog.objects.create(user=user, action_type='SERVICE_UPDATE', entity_type='ServiceRecord', entity_id=record.id, description=f'Updated service record for {record.machine.machine_code}')
    return record
