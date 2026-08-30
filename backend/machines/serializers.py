from rest_framework import serializers
from clients.models import Client
from .models import Machine, MachineAssignment
class MachineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Machine; fields = '__all__'; read_only_fields = ('id', 'created_at', 'updated_at')
class AssignmentSerializer(serializers.ModelSerializer):
    machine_code = serializers.CharField(source='machine.machine_code', read_only=True)
    client_name = serializers.CharField(source='client.client_name', read_only=True)
    machine_id = serializers.PrimaryKeyRelatedField(source='machine', queryset=Machine.objects.all(), write_only=True)
    client_id = serializers.PrimaryKeyRelatedField(source='client', queryset=Client.objects.all(), write_only=True)
    class Meta:
        model = MachineAssignment
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at', 'machine_code', 'client_name', 'assignment_status', 'returned_date')

    def validate_client_id(self, client):
        if client.status != 'ACTIVE':
            raise serializers.ValidationError('Only active clients can receive machines.')
        return client

class ReturnAssignmentSerializer(serializers.Serializer):
    returned_date = serializers.DateField()
    notes = serializers.CharField(required=False, allow_blank=True)

    def validate_returned_date(self, value):
        assignment = self.context['assignment']
        if value < assignment.assigned_date:
            raise serializers.ValidationError('Return date cannot precede assignment date.')
        return value
