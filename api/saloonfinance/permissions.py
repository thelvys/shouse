from rest_framework import permissions
from saloon.models import Salon

class IsSalonOwnerForFinance(permissions.BasePermission):
    def has_permission(self, request, view):
        return Salon.objects.filter(owner=request.user).exists()

    def has_object_permission(self, request, view, obj):
        return obj.salon.owner == request.user