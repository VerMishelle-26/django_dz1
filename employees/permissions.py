from rest_framework.permissions import BasePermission, SAFE_METHODS


class RoleBasedPermission(BasePermission):
    """
    Посетитель   — только чтение (SAFE_METHODS).
    Смотритель   — чтение + PATCH (перемещение между столами).
    Администратор — всё (CRUD).
    """

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return request.method in SAFE_METHODS

        if request.user.is_superuser or request.user.groups.filter(
            name="Администратор"
        ).exists():
            return True

        if request.user.groups.filter(name="Смотритель").exists():
            return request.method in SAFE_METHODS or request.method in ("PATCH", "PUT")

        return request.method in SAFE_METHODS