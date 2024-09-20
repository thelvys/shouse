from django.urls import path
from . import views

app_name = 'saloonfinance'

urlpatterns = [
    # Currency URLs
    path('currencies/', views.CurrencyListView.as_view(), name='currency_list'),
    path('currencies/create/', views.CurrencyCreateView.as_view(), name='currency_create'),
    path('currencies/<int:pk>/update/', views.CurrencyUpdateView.as_view(), name='currency_update'),
    path('currencies/<int:pk>/delete/', views.CurrencyDeleteView.as_view(), name='currency_delete'),

    # PaymentType URLs
    path('payment-types/', views.PaymentTypeListView.as_view(), name='paymenttype_list'),
    path('payment-types/create/', views.PaymentTypeCreateView.as_view(), name='paymenttype_create'),
    path('payment-types/<int:pk>/update/', views.PaymentTypeUpdateView.as_view(), name='paymenttype_update'),
    path('payment-types/<int:pk>/delete/', views.PaymentTypeDeleteView.as_view(), name='paymenttype_delete'),

    # CashRegister URLs
    path('salon/<int:salon_id>/cash-registers/', views.CashRegisterListView.as_view(), name='cashregister_list'),
    path('salon/<int:salon_id>/cash-registers/create/', views.CashRegisterCreateView.as_view(), name='cashregister_create'),
    path('salon/<int:salon_id>/cash-registers/<int:pk>/update/', views.CashRegisterUpdateView.as_view(), name='cashregister_update'),
    path('salon/<int:salon_id>/cash-registers/<int:pk>/delete/', views.CashRegisterDeleteView.as_view(), name='cashregister_delete'),

    # Payment URLs
    path('salon/<int:salon_id>/payments/', views.PaymentListView.as_view(), name='payment_list'),
    path('salon/<int:salon_id>/payments/create/', views.PaymentCreateView.as_view(), name='payment_create'),
    path('salon/<int:salon_id>/payments/<int:pk>/update/', views.PaymentUpdateView.as_view(), name='payment_update'),
    path('salon/<int:salon_id>/payments/<int:pk>/delete/', views.PaymentDeleteView.as_view(), name='payment_delete'),

    # Transaction URLs
    path('salon/<int:salon_id>/transactions/', views.TransactionListView.as_view(), name='transaction_list'),
    path('salon/<int:salon_id>/transactions/create/', views.TransactionCreateView.as_view(), name='transaction_create'),
    path('salon/<int:salon_id>/transactions/<int:pk>/update/', views.TransactionUpdateView.as_view(), name='transaction_update'),
    path('salon/<int:salon_id>/transactions/<int:pk>/delete/', views.TransactionDeleteView.as_view(), name='transaction_delete'),
]