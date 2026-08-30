from decimal import Decimal
from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APITestCase
from common.exceptions import ConflictError
from .models import InventoryItem
from .services import record_stock_in, record_stock_out

class InventoryTests(TestCase):
	def setUp(self):
		self.user = get_user_model().objects.create_user(username='tester', password='pass')
		self.item = InventoryItem.objects.create(item_code='INV-0001', item_name='Beans', category='CONSUMABLE', unit='kg', current_quantity=Decimal('10'), minimum_stock_level=Decimal('2'))

	def test_stock_in_and_out(self):
		record_stock_in(item_id=self.item.id, quantity='5', user=self.user); record_stock_out(item_id=self.item.id, quantity='3', user=self.user)
		self.item.refresh_from_db(); self.assertEqual(self.item.current_quantity, Decimal('12'))

	def test_stock_out_cannot_go_negative(self):
		with self.assertRaises(ConflictError): record_stock_out(item_id=self.item.id, quantity='11', user=self.user)

	def test_nonpositive_operations_are_rejected(self):
		for quantity in ('0', '-1'):
			with self.assertRaises(ConflictError): record_stock_in(item_id=self.item.id, quantity=quantity, user=self.user)


class InventoryAPITests(APITestCase):
	def setUp(self):
		user = get_user_model().objects.create_user(username='inventory-api', password='pass')
		self.client.force_authenticate(user)
		self.item = InventoryItem.objects.create(item_code='INV-API', item_name='API Item', category='OTHER', unit='unit', current_quantity=10, minimum_stock_level=2)

	def test_invalid_stock_quantities_return_400(self):
		for quantity in ('0', '-1', 'invalid'):
			response = self.client.post(f'/api/v1/inventory/{self.item.id}/stock-in/', {'quantity': quantity}, format='json')
			self.assertEqual(response.status_code, 400)
