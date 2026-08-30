from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, inline_serializer

class MeView(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(responses=inline_serializer(name='CurrentUser', fields={'id': serializers.IntegerField(), 'username': serializers.CharField(), 'email': serializers.EmailField(), 'first_name': serializers.CharField(), 'last_name': serializers.CharField()}))
    def get(self, request):
        return Response({'id': request.user.id, 'username': request.user.username, 'email': request.user.email, 'first_name': request.user.first_name, 'last_name': request.user.last_name})
