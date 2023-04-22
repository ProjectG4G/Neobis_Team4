from rest_framework import permissions
from rest_framework.permissions import BasePermission

from .models import CartItem


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if isinstance(obj, CartItem):
            return obj.cart.user == request.user

        return obj.user == request.user


class IsSupplierOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)
