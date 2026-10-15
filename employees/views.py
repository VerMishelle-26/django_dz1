from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render

from .models import Employee


def home(request):
    """Главная: количество + 4 последних сотрудника (К3, К4)."""
    total = Employee.objects.count()
    employees = (
        Employee.objects.select_related("user", "workplace")
        .prefetch_related("skills", "images")
        .order_by("-hire_date")[:4]
    )
    return render(
        request,
        "employees/home.html",
        {"employees": employees, "total": total},
    )


def employee_list(request):
    """Список с пагинацией по 10 (К5)."""
    queryset = (
        Employee.objects.select_related("user", "workplace")
        .prefetch_related("skills", "images")
        .order_by("-hire_date")
    )
    paginator = Paginator(queryset, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "employees/employee_list.html", {"page_obj": page_obj})


@login_required
def employee_detail(request, pk):
    """Подробная карточка (К6, К7)."""
    employee = get_object_or_404(
        Employee.objects.select_related("user", "workplace").prefetch_related(
            "skills", "images"
        ),
        pk=pk,
    )
    return render(
        request,
        "employees/employee_detail.html",
        {"employee": employee},
    )
