from rest_framework import permissions

from .models import User


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.is_staff or request.user.role == User.UserRole.ADMIN
        return False


class IsAuthorOrModOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
                request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated
                and (
                        obj.author == request.user
                        or request.user.is_staff
                        or request.user.role == User.UserRole.ADMIN
                        or request.user.role == User.UserRole.MODERATOR
                )
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated
                and (
                        request.user.is_staff
                        or request.user.role == User.UserRole.ADMIN
                )
        )
