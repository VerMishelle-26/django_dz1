from rest_framework import serializers
from .models import Workplace


class WorkplaceSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source="employee.__str__", read_only=True)

    class Meta:
        model = Workplace
        fields = ["id", "desk_number", "description", "employee", "employee_name"]