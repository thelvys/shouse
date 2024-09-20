from rest_framework import viewsets, permissions
from saloonservices.models import HairstyleTariffHistory, Hairstyle, Shave
from .serializers import HairstyleTariffHistorySerializer, HairstyleSerializer, ShaveSerializer
from .permissions import IsSalonOwnerForServices
from saloon.models import Salon

class HairstyleViewSet(viewsets.ModelViewSet):
    serializer_class = HairstyleSerializer
    permission_classes = [permissions.IsAuthenticated, IsSalonOwnerForServices]

    def get_queryset(self):
        return Hairstyle.objects.filter(salon__owner=self.request.user)

    def perform_create(self, serializer):
        salon = Salon.objects.get(owner=self.request.user)
        serializer.save(salon=salon)

class HairstyleTariffHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = HairstyleTariffHistorySerializer
    permission_classes = [permissions.IsAuthenticated, IsSalonOwnerForServices]

    def get_queryset(self):
        return HairstyleTariffHistory.objects.filter(hairstyle__salon__owner=self.request.user)

class ShaveViewSet(viewsets.ModelViewSet):
    serializer_class = ShaveSerializer
    permission_classes = [permissions.IsAuthenticated, IsSalonOwnerForServices]

    def get_queryset(self):
        return Shave.objects.filter(salon__owner=self.request.user)

    def perform_create(self, serializer):
        salon = Salon.objects.get(owner=self.request.user)
        serializer.save(salon=salon)