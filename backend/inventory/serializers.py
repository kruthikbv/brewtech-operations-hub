from decimal import Decimal

from rest_framework import serializers
from .models import InventoryItem, InventoryTransaction
class InventoryItemSerializer(serializers.ModelSerializer):
    is_low_stock = serializers.ReadOnlyField()
    class Meta:
        model = InventoryItem; fields = '__all__'; read_only_fields = ('id', 'created_at', 'updated_at', 'is_low_stock')
class InventoryTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryTransaction
        fields = '__all__'
        read_only_fields = ('id', 'created_at')

class StockOperationSerializer(serializers.Serializer):
    quantity = serializers.DecimalField(max_digits=12, decimal_places=2, min_value=Decimal('0.01'))
    remarks = serializers.CharField(required=False, allow_blank=True)
