from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("employees/", views.employee_list, name="employee_list"),
    path("employees/<int:pk>/", views.employee_detail, name="employee_detail"),
]

from rest_framework.routers import DefaultRouter
from .views import EmployeeViewSet, SkillViewSet

router = DefaultRouter()
router.register("employees", EmployeeViewSet)
router.register("skills", SkillViewSet)

urlpatterns = router.urls