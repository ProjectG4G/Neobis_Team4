from rest_framework.permissions import SAFE_METHODS, BasePermission
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
        if request.user.is_authenticated and request.user.is_staff:
            return True
        else:
            permission_classes = [IsAdminUser]

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.user.is_superuser:
            return True

        if request.user.is_staff and isinstance(obj, User):
            return not obj.is_superuser
