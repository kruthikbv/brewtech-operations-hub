from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import ActivityLog
from .serializers import ActivityLogSerializer
class ActivityLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ActivityLog.objects.all(); serializer_class = ActivityLogSerializer; permission_classes = [IsAuthenticated]
