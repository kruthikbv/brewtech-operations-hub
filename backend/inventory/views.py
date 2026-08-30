from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import InventoryItem, InventoryTransaction
from .serializers import InventoryItemSerializer, InventoryTransactionSerializer, StockOperationSerializer
from .services import record_stock_in, record_stock_out


class InventoryViewSet(viewsets.ModelViewSet):
    queryset = InventoryItem.objects.all().order_by('item_name')
    serializer_class = InventoryItemSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['category']
    search_fields = ['item_code', 'item_name']
    ordering_fields = ['item_name', 'current_quantity']

    @action(detail=True, methods=['post'], url_path='stock-in')
    def stock_in(self, request, pk=None):
        return self._stock(request, record_stock_in)

    @action(detail=True, methods=['post'], url_path='stock-out')
    def stock_out(self, request, pk=None):
        return self._stock(request, record_stock_out)

    def _stock(self, request, operation):
        item = self.get_object()
        serializer = StockOperationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        record = operation(item_id=item.id, user=request.user, **serializer.validated_data)
        return Response(InventoryTransactionSerializer(record).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'])
    def transactions(self, request, pk=None):
        item = self.get_object()
        queryset = InventoryTransaction.objects.filter(inventory_item=item).order_by('-transaction_date', '-created_at')
        page = self.paginate_queryset(queryset)
        serializer = InventoryTransactionSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)
