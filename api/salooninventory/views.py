from rest_framework import viewsets, permissions
from salooninventory.models import Item, ItemUsed, ItemPurchase
from .serializers import ItemSerializer, ItemUsedSerializer, ItemPurchaseSerializer
from .permissions import IsSalonOwnerForInventory
from saloon.models import Salon

class ItemViewSet(viewsets.ModelViewSet):
    serializer_class = ItemSerializer
    permission_classes = [permissions.IsAuthenticated, IsSalonOwnerForInventory]

    def get_queryset(self):
        return Item.objects.filter(salon__owner=self.request.user)

    def perform_create(self, serializer):
        salon = Salon.objects.get(owner=self.request.user)
        serializer.save(salon=salon)

class ItemUsedViewSet(viewsets.ModelViewSet):
    serializer_class = ItemUsedSerializer
    permission_classes = [permissions.IsAuthenticated, IsSalonOwnerForInventory]

    def get_queryset(self):
        return ItemUsed.objects.filter(salon__owner=self.request.user)

    def perform_create(self, serializer):
        salon = Salon.objects.get(owner=self.request.user)
        serializer.save(salon=salon)

class ItemPurchaseViewSet(viewsets.ModelViewSet):
    serializer_class = ItemPurchaseSerializer
    permission_classes = [permissions.IsAuthenticated, IsSalonOwnerForInventory]

    def get_queryset(self):
        return ItemPurchase.objects.filter(salon__owner=self.request.user)

    def perform_create(self, serializer):
        salon = Salon.objects.get(owner=self.request.user)
        serializer.save(salon=salon)