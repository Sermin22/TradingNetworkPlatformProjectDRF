from rest_framework import permissions


class IsActiveEmployee(permissions.BasePermission):
    """Класс возвращает аутентифицированных активных юзеров, которые являются сотрудниками"""
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_active and request.user.is_staff
