from django.test import TestCase
from .models import Client

class ClientTests(TestCase):
	def test_create_and_update_client(self):
		client = Client.objects.create(client_code='CLT-0001', client_name='Test Client')
		client.client_name = 'Updated Client'; client.save()
		self.assertEqual(Client.objects.get(pk=client.pk).client_name, 'Updated Client')

	def test_duplicate_code_rejected(self):
		Client.objects.create(client_code='CLT-0001', client_name='First')
		with self.assertRaises(Exception): Client.objects.create(client_code='CLT-0001', client_name='Second')
