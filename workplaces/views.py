from rest_framework import viewsets
from .models import Workplace
from .serializers import WorkplaceSerializer
from employees.permissions import RoleBasedPermission


class WorkplaceViewSet(viewsets.ModelViewSet):
    queryset = Workplace.objects.select_related("employee")
    serializer_class = WorkplaceSerializer
    permission_classes = [RoleBasedPermission]