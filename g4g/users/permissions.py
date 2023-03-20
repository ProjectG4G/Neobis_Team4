from rest_framework import permissions
from .models import User


class IsProfileOwnerOrAdmin(permissions.BasePermission):
    """
    Object-level permission to only allow updating his own profile
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.is_staff:
            return True

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.user.is_superuser or request.user.is_staff:
            return True
        if request.user.pk == obj.pk:
            return True


class IsStaff(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.is_staff:
            return True

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.user.is_superuser:
            return True

        if request.user.is_staff and isinstance(obj, User):
            return not obj.is_superuser
