from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase

from machines.models import Machine
from .services import create_service_record, update_service_record


class ServiceRecordTests(TestCase):
	def setUp(self):
		self.user = get_user_model().objects.create_user(username='service-user', password='pass')
		self.machine = Machine.objects.create(machine_code='MCH-SVC', machine_model='Model S', serial_number='SN-SVC', purchase_date=date.today(), status='DEPLOYED')
		self.data = {'machine': self.machine, 'service_date': date.today(), 'service_type': 'REPAIR', 'technician_name': 'Demo Technician', 'description': 'Synthetic repair', 'status': 'IN_PROGRESS'}

	def test_completed_service_restores_machine_status(self):
		record = create_service_record(data=self.data.copy(), user=self.user)
		self.machine.refresh_from_db(); self.assertEqual(self.machine.status, 'UNDER_SERVICE')
		update_service_record(record=record, data={'status': 'COMPLETED'}, user=self.user)
		self.machine.refresh_from_db(); self.assertEqual(self.machine.status, 'DEPLOYED')

	def test_cancelled_service_restores_machine_status(self):
		record = create_service_record(data=self.data.copy(), user=self.user)
		update_service_record(record=record, data={'status': 'CANCELLED'}, user=self.user)
		self.machine.refresh_from_db(); self.assertEqual(self.machine.status, 'DEPLOYED')
