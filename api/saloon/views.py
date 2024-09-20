from rest_framework import viewsets, permissions
from saloon.models import Salon, Barber, Client, BarberType, Attachment
from .serializers import SalonSerializer, BarberSerializer, ClientSerializer, BarberTypeSerializer, AttachmentSerializer
from .permissions import IsSalonOwner, IsSalonOwnerForRelatedObjects

class SalonViewSet(viewsets.ModelViewSet):
    serializer_class = SalonSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Salon.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.IsAuthenticated()]
        return [permissions.IsAuthenticated(), IsSalonOwner()]

class BarberTypeViewSet(viewsets.ModelViewSet):
    serializer_class = BarberTypeSerializer
    permission_classes = [permissions.IsAuthenticated, IsSalonOwnerForRelatedObjects]

    def get_queryset(self):
        return BarberType.objects.filter(salon__owner=self.request.user)

    def perform_create(self, serializer):
        salon = Salon.objects.get(owner=self.request.user)
        serializer.save(salon=salon)

class BarberViewSet(viewsets.ModelViewSet):
    serializer_class = BarberSerializer
    permission_classes = [permissions.IsAuthenticated, IsSalonOwnerForRelatedObjects]

    def get_queryset(self):
        return Barber.objects.filter(salon__owner=self.request.user)

class ClientViewSet(viewsets.ModelViewSet):
    serializer_class = ClientSerializer
    permission_classes = [permissions.IsAuthenticated, IsSalonOwnerForRelatedObjects]

    def get_queryset(self):
        return Client.objects.filter(salon__owner=self.request.user)

class AttachmentViewSet(viewsets.ModelViewSet):
    serializer_class = AttachmentSerializer
    permission_classes = [permissions.IsAuthenticated, IsSalonOwnerForRelatedObjects]

    def get_queryset(self):
        return Attachment.objects.filter(salon__owner=self.request.user)