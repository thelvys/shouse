from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CurrencyViewSet, CashRegisterViewSet, PaymentTypeViewSet, PaymentViewSet, TransactionViewSet

router = DefaultRouter()
router.register(r'currencies', CurrencyViewSet)
router.register(r'cash-registers', CashRegisterViewSet, basename='cashregister')
router.register(r'payment-types', PaymentTypeViewSet)
router.register(r'payments', PaymentViewSet, basename='payment')
router.register(r'transactions', TransactionViewSet, basename='transaction')

urlpatterns = [
    path('', include(router.urls)),
]