from django.contrib import admin
from .models import Employee, Skill


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "level")
    list_filter = ("level",)
    search_fields = ("name",)


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("id", "last_name", "first_name", "gender", "user")
    list_filter = ("gender",)
    search_fields = ("last_name", "first_name", "user__username")
    filter_horizontal = ("skills",)