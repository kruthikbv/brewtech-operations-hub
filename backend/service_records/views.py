from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import ServiceRecord
from .serializers import ServiceRecordSerializer
from .services import create_service_record, update_service_record
class ServiceRecordViewSet(viewsets.ModelViewSet):
    queryset = ServiceRecord.objects.select_related('machine').all().order_by('-service_date'); serializer_class = ServiceRecordSerializer; permission_classes = [IsAuthenticated]
    filterset_fields = ['machine', 'service_type', 'status', 'service_date']
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data); serializer.is_valid(raise_exception=True); record = create_service_record(data=serializer.validated_data, user=request.user); return Response(self.get_serializer(record).data, status=status.HTTP_201_CREATED)
    def update(self, request, *args, **kwargs):
        record = self.get_object(); serializer = self.get_serializer(record, data=request.data, partial=kwargs.pop('partial', False)); serializer.is_valid(raise_exception=True); result = update_service_record(record=record, data=serializer.validated_data, user=request.user); return Response(self.get_serializer(result).data)
