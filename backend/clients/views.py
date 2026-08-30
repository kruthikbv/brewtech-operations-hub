from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from activity_logs.models import ActivityLog
from .models import Client
from .serializers import ClientSerializer
class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all().order_by('client_name')
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['status', 'city']
    search_fields = ['client_code', 'client_name', 'contact_person']
    ordering_fields = ['client_name', 'created_at', 'status']
    def perform_create(self, serializer):
        client = serializer.save()
        ActivityLog.objects.create(user=self.request.user, action_type='CREATE', entity_type='Client', entity_id=client.id, description=f'Created client {client.client_code}')
    def perform_update(self, serializer):
        client = serializer.save()
        ActivityLog.objects.create(user=self.request.user, action_type='UPDATE', entity_type='Client', entity_id=client.id, description=f'Updated client {client.client_code}')
    def destroy(self, request, *args, **kwargs):
        client = self.get_object(); client.status = 'INACTIVE'; client.save(update_fields=['status', 'updated_at'])
        ActivityLog.objects.create(user=request.user, action_type='DEACTIVATE', entity_type='Client', entity_id=client.id, description=f'Deactivated client {client.client_code}')
        return Response(status=204)
