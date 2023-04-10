from rest_framework.permissions import SAFE_METHODS, BasePermission, IsAdminUser
from .models import User


class IsProfileOwnerOrAdmin(BasePermission):
    """
    Object-level permission to only allow updating his own profile
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if obj.id == request.user.id:
            return True
        if request.user.is_staff:
            return True
        return False


class IsStaff(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff


class IsSuperuser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_superuser
