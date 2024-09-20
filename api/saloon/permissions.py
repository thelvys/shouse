from rest_framework import permissions
from saloon.models import Salon

class IsSalonOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user

class IsSalonOwnerForRelatedObjects(permissions.BasePermission):
    def has_permission(self, request, view):
        return Salon.objects.filter(owner=request.user).exists()

    def has_object_permission(self, request, view, obj):
        return obj.salon.owner == request.user