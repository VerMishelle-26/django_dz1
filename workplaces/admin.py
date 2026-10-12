from django.contrib import admin
from .models import Workplace


@admin.register(Workplace)
class WorkplaceAdmin(admin.ModelAdmin):
    list_display = ("id", "desk_number", "employee")
    search_fields = ("desk_number",)