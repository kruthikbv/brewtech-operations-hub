from rest_framework import serializers
from .models import ServiceRecord
class ServiceRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceRecord; fields = '__all__'; read_only_fields = ('id', 'created_at', 'updated_at', 'previous_machine_status')

    def validate_machine(self, machine):
        if self.instance and machine != self.instance.machine:
            raise serializers.ValidationError('The machine on a service record cannot be changed.')
        return machine
