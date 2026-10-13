from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render

from .models import Employee


def home(request):
    """Главная страница."""
    employees = Employee.objects.prefetch_related("skills").all()[:4]
    return render(request, "employees/home.html", {"employees": employees})


def employee_list(request):
    """Список сотрудников."""
    employees = Employee.objects.prefetch_related("skills").all()
    return render(request, "employees/employee_list.html", {"employees": employees})


@login_required
def employee_detail(request, pk):
    """Подробная карточка (только для авторизованных)."""
    employee = get_object_or_404(
        Employee.objects.prefetch_related("skills", "images"), pk=pk
    )
    return render(request, "employees/employee_detail.html", {"employee": employee})
