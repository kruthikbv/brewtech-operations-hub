from rest_framework.permissions import IsAuthenticated

class AuthenticatedOperationPermission(IsAuthenticated):
    pass
