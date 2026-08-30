from datetime import date
from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APITestCase
from clients.models import Client
from common.exceptions import ConflictError
from .models import Machine
from .services import assign_machine, return_machine

class MachineTests(TestCase):
	def setUp(self):
		self.user = get_user_model().objects.create_user(username='tester', password='pass')
		self.client = Client.objects.create(client_code='CLT-0001', client_name='Test Client')
		self.machine = Machine.objects.create(machine_code='MCH-0001', machine_model='Model A', serial_number='SN-0001', purchase_date=date.today())

	def test_assign_and_return_machine(self):
		assignment = assign_machine(machine_id=self.machine.id, client=self.client, assigned_date=date.today(), user=self.user)
		self.machine.refresh_from_db(); self.assertEqual(self.machine.status, 'DEPLOYED')
		return_machine(assignment=assignment, returned_date=date.today(), user=self.user)
		self.machine.refresh_from_db(); self.assertEqual(self.machine.status, 'AVAILABLE')

	def test_unavailable_machine_rejected(self):
		self.machine.status = 'DEPLOYED'; self.machine.save()
		with self.assertRaises(ConflictError): assign_machine(machine_id=self.machine.id, client=self.client, assigned_date=date.today(), user=self.user)

	def test_inactive_client_rejected(self):
		self.client.status = 'INACTIVE'; self.client.save()
		with self.assertRaises(ConflictError): assign_machine(machine_id=self.machine.id, client=self.client, assigned_date=date.today(), user=self.user)


class AssignmentAPITests(APITestCase):
	def setUp(self):
		self.user = get_user_model().objects.create_user(username='api-user', password='pass')
		self.client.force_authenticate(self.user)
		client = Client.objects.create(client_code='CLT-API', client_name='API Client')
		machine = Machine.objects.create(machine_code='MCH-API', machine_model='API Model', serial_number='SN-API', purchase_date=date.today())
		self.assignment = assign_machine(machine_id=machine.id, client=client, assigned_date=date.today(), user=self.user)

	def test_documented_return_route(self):
		response = self.client.post(f'/api/v1/assignments/{self.assignment.id}/return/', {'returned_date': date.today().isoformat()}, format='json')
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.data['assignment_status'], 'RETURNED')
