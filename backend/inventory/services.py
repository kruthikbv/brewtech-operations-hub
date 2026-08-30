from django.db import transaction
from django.utils import timezone
from decimal import Decimal
from common.exceptions import ConflictError
from activity_logs.models import ActivityLog
from common.constants import STOCK_IN, STOCK_OUT
from .models import InventoryItem, InventoryTransaction

def _record(*, item_id, quantity, transaction_type, remarks='', user=None):
    with transaction.atomic():
        item = InventoryItem.objects.select_for_update().get(pk=item_id)
        quantity = Decimal(str(quantity))
        if quantity <= 0:
            raise ConflictError('Quantity must be greater than zero.')
        if transaction_type == STOCK_OUT and quantity > item.current_quantity: raise ConflictError('Stock-out quantity exceeds current inventory.')
        item.current_quantity += quantity if transaction_type == STOCK_IN else -quantity; item.save(update_fields=['current_quantity', 'updated_at'])
        record = InventoryTransaction.objects.create(inventory_item=item, transaction_type=transaction_type, quantity=quantity, transaction_date=timezone.localdate(), remarks=remarks)
        ActivityLog.objects.create(user=user, action_type=transaction_type, entity_type='InventoryItem', entity_id=item.id, description=f'Recorded {transaction_type.lower().replace("_", " ")} for {item.item_code}')
        return record

def record_stock_in(*, item_id, quantity, remarks='', user=None): return _record(item_id=item_id, quantity=quantity, transaction_type=STOCK_IN, remarks=remarks, user=user)
def record_stock_out(*, item_id, quantity, remarks='', user=None): return _record(item_id=item_id, quantity=quantity, transaction_type=STOCK_OUT, remarks=remarks, user=user)
