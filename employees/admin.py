from django.contrib import admin

from .models import Employee, EmployeeImage, Skill


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "level")
    list_filter = ("level",)
    search_fields = ("name",)


class EmployeeImageInline(admin.TabularInline):
    model = EmployeeImage
    extra = 1


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("id", "last_name", "first_name", "gender", "user")
    list_filter = ("gender",)
    search_fields = ("last_name", "first_name", "user__username")
    filter_horizontal = ("skills",)
    inlines = [EmployeeImageInline]


@admin.register(EmployeeImage)
class EmployeeImageAdmin(admin.ModelAdmin):
    list_display = ("id", "employee", "order")
