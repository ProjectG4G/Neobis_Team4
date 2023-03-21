from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import TrainingsApplications


class IsAdminOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        if request.method in SAFE_METHODS:
            return True

        return bool(request.user.is_staff)

    def has_object_permission(self, request, view, obj):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        if request.method in SAFE_METHODS:
            return True
        if isinstance(obj, TrainingsApplications):
            return bool(request.user == obj.user)

        return bool(request.user.is_staff)
