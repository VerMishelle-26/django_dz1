from django.contrib import admin

from .models import Employee, EmployeeImage, Skill


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "level")
    list_filter = ("level",)


class EmployeeImageInline(admin.TabularInline):
    model = EmployeeImage
    extra = 1


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("id", "last_name", "first_name", "role", "gender", "user")
    list_filter = ("role", "gender")
    filter_horizontal = ("skills",)
    inlines = [EmployeeImageInline]

    def save_model(self, request, obj, form, change):
        obj.full_clean()  # вызывает clean()
        super().save_model(request, obj, form, change)


@admin.register(EmployeeImage)
class EmployeeImageAdmin(admin.ModelAdmin):
    list_display = ("id", "employee", "order")
