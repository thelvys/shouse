from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from saloon.models import Salon
from .models import Currency, CashRegister, PaymentType, Payment, Transaction
from .forms import CurrencyForm, CashRegisterForm, PaymentTypeForm, PaymentForm, TransactionForm

class SalonOwnerMixin(UserPassesTestMixin):
    def test_func(self):
        salon_id = self.kwargs.get('salon_id')
        return self.request.user.owned_salons.filter(id=salon_id).exists()

class CurrencyListView(LoginRequiredMixin, ListView):
    model = Currency
    template_name = 'saloonfinance/currency_list.html'
    context_object_name = 'currencies'

class CurrencyCreateView(LoginRequiredMixin, CreateView):
    model = Currency
    form_class = CurrencyForm
    template_name = 'saloonfinance/currency_form.html'
    success_url = reverse_lazy('saloonfinance:currency_list')

class CurrencyUpdateView(LoginRequiredMixin, UpdateView):
    model = Currency
    form_class = CurrencyForm
    template_name = 'saloonfinance/currency_form.html'
    success_url = reverse_lazy('saloonfinance:currency_list')

class CurrencyDeleteView(LoginRequiredMixin, DeleteView):
    model = Currency
    template_name = 'saloonfinance/currency_confirm_delete.html'
    success_url = reverse_lazy('saloonfinance:currency_list')

class CashRegisterListView(LoginRequiredMixin, SalonOwnerMixin, ListView):
    model = CashRegister
    template_name = 'saloonfinance/cashregister_list.html'
    context_object_name = 'cash_registers'

    def get_queryset(self):
        salon = get_object_or_404(Salon, pk=self.kwargs['salon_id'])
        return CashRegister.objects.filter(salon=salon)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['salon'] = self.salon
        return context

class CashRegisterCreateView(LoginRequiredMixin, SalonOwnerMixin, CreateView):
    model = CashRegister
    form_class = CashRegisterForm
    template_name = 'saloonfinance/cashregister_form.html'

    def get_success_url(self):
        return reverse_lazy('saloonfinance:cashregister_list', kwargs={'salon_id': self.kwargs['salon_id']})

    def form_valid(self, form):
        form.instance.salon = get_object_or_404(Salon, pk=self.kwargs['salon_id'])
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['salon'] = self.salon
        return context

class CashRegisterUpdateView(LoginRequiredMixin, SalonOwnerMixin, UpdateView):
    model = CashRegister
    form_class = CashRegisterForm
    template_name = 'saloonfinance/cashregister_form.html'

    def get_success_url(self):
        return reverse_lazy('saloonfinance:cashregister_list', kwargs={'salon_id': self.object.salon.id})

class CashRegisterDeleteView(LoginRequiredMixin, SalonOwnerMixin, DeleteView):
    model = CashRegister
    template_name = 'saloonfinance/cashregister_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('saloonfinance:cashregister_list', kwargs={'salon_id': self.object.salon.id})

class PaymentTypeListView(LoginRequiredMixin, ListView):
    model = PaymentType
    template_name = 'saloonfinance/paymenttype_list.html'
    context_object_name = 'payment_types'

class PaymentTypeCreateView(LoginRequiredMixin, CreateView):
    model = PaymentType
    form_class = PaymentTypeForm
    template_name = 'saloonfinance/paymenttype_form.html'
    success_url = reverse_lazy('saloonfinance:paymenttype_list')

class PaymentTypeUpdateView(LoginRequiredMixin, UpdateView):
    model = PaymentType
    form_class = PaymentTypeForm
    template_name = 'saloonfinance/paymenttype_form.html'
    success_url = reverse_lazy('saloonfinance:paymenttype_list')

class PaymentTypeDeleteView(LoginRequiredMixin, DeleteView):
    model = PaymentType
    template_name = 'saloonfinance/paymenttype_confirm_delete.html'
    success_url = reverse_lazy('saloonfinance:paymenttype_list')

class PaymentListView(LoginRequiredMixin, SalonOwnerMixin, ListView):
    model = Payment
    template_name = 'saloonfinance/payment_list.html'
    context_object_name = 'payments'

    def get_queryset(self):
        salon = get_object_or_404(Salon, pk=self.kwargs['salon_id'])
        return Payment.objects.filter(salon=salon)

class PaymentCreateView(LoginRequiredMixin, SalonOwnerMixin, CreateView):
    model = Payment
    form_class = PaymentForm
    template_name = 'saloonfinance/payment_form.html'

    def get_success_url(self):
        return reverse_lazy('saloonfinance:payment_list', kwargs={'salon_id': self.kwargs['salon_id']})

    def form_valid(self, form):
        form.instance.salon = get_object_or_404(Salon, pk=self.kwargs['salon_id'])
        return super().form_valid(form)

class PaymentUpdateView(LoginRequiredMixin, SalonOwnerMixin, UpdateView):
    model = Payment
    form_class = PaymentForm
    template_name = 'saloonfinance/payment_form.html'

    def get_success_url(self):
        return reverse_lazy('saloonfinance:payment_list', kwargs={'salon_id': self.object.salon.id})

class PaymentDeleteView(LoginRequiredMixin, SalonOwnerMixin, DeleteView):
    model = Payment
    template_name = 'saloonfinance/payment_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('saloonfinance:payment_list', kwargs={'salon_id': self.object.salon.id})

class TransactionListView(LoginRequiredMixin, SalonOwnerMixin, ListView):
    model = Transaction
    template_name = 'saloonfinance/transaction_list.html'
    context_object_name = 'transactions'

    def get_queryset(self):
        salon = get_object_or_404(Salon, pk=self.kwargs['salon_id'])
        return Transaction.objects.filter(salon=salon)

class TransactionCreateView(LoginRequiredMixin, SalonOwnerMixin, CreateView):
    model = Transaction
    form_class = TransactionForm
    template_name = 'saloonfinance/transaction_form.html'

    def get_success_url(self):
        return reverse_lazy('saloonfinance:transaction_list', kwargs={'salon_id': self.kwargs['salon_id']})

    def form_valid(self, form):
        form.instance.salon = get_object_or_404(Salon, pk=self.kwargs['salon_id'])
        return super().form_valid(form)

class TransactionUpdateView(LoginRequiredMixin, SalonOwnerMixin, UpdateView):
    model = Transaction
    form_class = TransactionForm
    template_name = 'saloonfinance/transaction_form.html'

    def get_success_url(self):
        return reverse_lazy('saloonfinance:transaction_list', kwargs={'salon_id': self.object.salon.id})

class TransactionDeleteView(LoginRequiredMixin, SalonOwnerMixin, DeleteView):
    model = Transaction
    template_name = 'saloonfinance/transaction_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('saloonfinance:transaction_list', kwargs={'salon_id': self.object.salon.id})