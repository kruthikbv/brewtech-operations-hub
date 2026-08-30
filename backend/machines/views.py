from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from activity_logs.models import ActivityLog
from .models import Machine, MachineAssignment
from .serializers import AssignmentSerializer, MachineSerializer, ReturnAssignmentSerializer
from .services import assign_machine, return_machine


class MachineViewSet(viewsets.ModelViewSet):
    queryset = Machine.objects.all().order_by('machine_code')
    serializer_class = MachineSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['status', 'machine_model']
    search_fields = ['machine_code', 'serial_number', 'machine_model']
    ordering_fields = ['machine_code', 'status']

    def perform_create(self, serializer):
        machine = serializer.save()
        ActivityLog.objects.create(user=self.request.user, action_type='CREATE', entity_type='Machine', entity_id=machine.id, description=f'Created machine {machine.machine_code}')

    def perform_update(self, serializer):
        machine = serializer.save()
        ActivityLog.objects.create(user=self.request.user, action_type='UPDATE', entity_type='Machine', entity_id=machine.id, description=f'Updated machine {machine.machine_code}')


class AssignmentViewSet(viewsets.ModelViewSet):
    queryset = MachineAssignment.objects.select_related('machine', 'client').all().order_by('-assigned_date')
    serializer_class = AssignmentSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['assignment_status', 'machine', 'client']
    http_method_names = ['get', 'post', 'head', 'options']

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        assignment = assign_machine(
            machine_id=serializer.validated_data['machine'].id,
            client=serializer.validated_data['client'],
            assigned_date=serializer.validated_data['assigned_date'],
            notes=serializer.validated_data.get('notes', ''),
            user=request.user,
        )
        return Response(self.get_serializer(assignment).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'], url_path='return')
    def return_assignment(self, request, pk=None):
        assignment = self.get_object()
        serializer = ReturnAssignmentSerializer(data=request.data, context={'assignment': assignment})
        serializer.is_valid(raise_exception=True)
        result = return_machine(assignment=assignment, user=request.user, **serializer.validated_data)
        return Response(self.get_serializer(result).data)
