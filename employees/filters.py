from django_filters import rest_framework as filters
from .models import Employee


class EmployeeFilter(filters.FilterSet):
    skills = filters.CharFilter(
        field_name="skills__name",
        lookup_expr="icontains",
        label="Навык (часть названия)",
    )
    min_experience_days = filters.NumberFilter(
        method="filter_min_experience",
        label="Минимальный стаж (дней)",
    )
    role = filters.CharFilter(field_name="role", lookup_expr="exact")

    class Meta:
        model = Employee
        fields = ["skills", "role", "min_experience_days"]

    def filter_min_experience(self, queryset, name, value):
        """Стаж = (сегодня - hire_date) >= value дней."""
        from datetime import date, timedelta

        cutoff = date.today() - timedelta(days=int(value))
        return queryset.filter(hire_date__lte=cutoff)