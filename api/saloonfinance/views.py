from rest_framework import viewsets, permissions
from saloonfinance.models import Currency, CashRegister, PaymentType, Payment, Transaction
from .serializers import CurrencySerializer, CashRegisterSerializer, PaymentTypeSerializer, PaymentSerializer, TransactionSerializer
from .permissions import IsSalonOwnerForFinance
from saloon.models import Salon

class CurrencyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
    permission_classes = [permissions.IsAuthenticated]

class CashRegisterViewSet(viewsets.ModelViewSet):
    serializer_class = CashRegisterSerializer
    permission_classes = [permissions.IsAuthenticated, IsSalonOwnerForFinance]

    def get_queryset(self):
        return CashRegister.objects.filter(salon__owner=self.request.user)

    def perform_create(self, serializer):
        salon = Salon.objects.get(owner=self.request.user)
        serializer.save(salon=salon)

class PaymentTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PaymentType.objects.all()
    serializer_class = PaymentTypeSerializer
    permission_classes = [permissions.IsAuthenticated]

class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated, IsSalonOwnerForFinance]

    def get_queryset(self):
        return Payment.objects.filter(salon__owner=self.request.user)

    def perform_create(self, serializer):
        salon = Salon.objects.get(owner=self.request.user)
        serializer.save(salon=salon)

class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated, IsSalonOwnerForFinance]

    def get_queryset(self):
        return Transaction.objects.filter(salon__owner=self.request.user)

    def perform_create(self, serializer):
        salon = Salon.objects.get(owner=self.request.user)
        serializer.save(salon=salon)