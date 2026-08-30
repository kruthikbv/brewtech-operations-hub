from django.db import models
from django.db.models import Count, Sum
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, inline_serializer
from clients.models import Client
from machines.models import Machine
from service_records.models import ServiceRecord
from inventory.models import InventoryItem
from activity_logs.models import ActivityLog

class SummaryView(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(responses=inline_serializer(name='DashboardSummary', fields={key: serializers.IntegerField() for key in ['total_clients', 'active_clients', 'total_machines', 'available_machines', 'deployed_machines', 'machines_under_service', 'low_stock_items']}))
    def get(self, request):
        return Response({'total_clients': Client.objects.count(), 'active_clients': Client.objects.filter(status='ACTIVE').count(), 'total_machines': Machine.objects.count(), 'available_machines': Machine.objects.filter(status='AVAILABLE').count(), 'deployed_machines': Machine.objects.filter(status='DEPLOYED').count(), 'machines_under_service': Machine.objects.filter(status='UNDER_SERVICE').count(), 'low_stock_items': InventoryItem.objects.filter(current_quantity__lte=models.F('minimum_stock_level')).count()})
class RecentActivityView(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(responses=inline_serializer(name='RecentActivity', many=True, fields={'id': serializers.IntegerField(), 'action_type': serializers.CharField(), 'entity_type': serializers.CharField(), 'entity_id': serializers.IntegerField(), 'description': serializers.CharField(), 'created_at': serializers.DateTimeField()}))
    def get(self, request):
        return Response(list(ActivityLog.objects.values('id', 'action_type', 'entity_type', 'entity_id', 'description', 'created_at')[:10]))
class MachineStatusView(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(responses=inline_serializer(name='MachineStatusAnalytics', many=True, fields={'status': serializers.CharField(), 'count': serializers.IntegerField()}))
    def get(self, request): return Response(list(Machine.objects.values('status').annotate(count=Count('id'))))
class MachinesPerClientView(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(responses=inline_serializer(name='MachinesPerClientAnalytics', many=True, fields={'client_name': serializers.CharField(), 'count': serializers.IntegerField()}))
    def get(self, request): return Response(list(Client.objects.filter(machine_assignments__assignment_status='ACTIVE').values('client_name').annotate(count=Count('machine_assignments'))))
class ServiceActivityView(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(responses=inline_serializer(name='ServiceActivityAnalytics', many=True, fields={'service_date': serializers.DateField(), 'count': serializers.IntegerField()}))
    def get(self, request): return Response(list(ServiceRecord.objects.values('service_date').annotate(count=Count('id')).order_by('service_date')))
class InventoryOverviewView(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(responses=inline_serializer(name='InventoryOverviewAnalytics', many=True, fields={'category': serializers.CharField(), 'quantity': serializers.DecimalField(max_digits=20, decimal_places=2)}))
    def get(self, request): return Response(list(InventoryItem.objects.values('category').annotate(quantity=Sum('current_quantity'))))
