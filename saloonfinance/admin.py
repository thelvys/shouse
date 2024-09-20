from django.contrib import admin
from .models import Currency, CashRegister, PaymentType, Payment, Transaction

class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'is_default')
    search_fields = ('code', 'name')

admin.site.register(Currency, CurrencyAdmin)

class CashRegisterAdmin(admin.ModelAdmin):
    list_display = ('name', 'balance', 'currency', 'salon')
    list_filter = ('salon', 'currency')
    search_fields = ('name', 'salon__name')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(salon__owner=request.user)

    def has_add_permission(self, request):
        return request.user.is_superuser or request.user.owned_salons.exists()

    def has_change_permission(self, request, obj=None):
        if obj is None:
            return True
        return obj.salon.owner == request.user or request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        if obj is None:
            return True
        return obj.salon.owner == request.user or request.user.is_superuser

admin.site.register(CashRegister, CashRegisterAdmin)

class PaymentTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)

admin.site.register(PaymentType, PaymentTypeAdmin)

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('barber', 'amount', 'currency', 'payment_type', 'date_payment', 'salon')
    list_filter = ('payment_type', 'salon', 'currency')
    search_fields = ('barber__user__email', 'salon__name')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(salon__owner=request.user)

    def has_add_permission(self, request):
        return request.user.is_superuser or request.user.owned_salons.exists()

    def has_change_permission(self, request, obj=None):
        if obj is None:
            return True
        return obj.salon.owner == request.user or request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        if obj is None:
            return True
        return obj.salon.owner == request.user or request.user.is_superuser

admin.site.register(Payment, PaymentAdmin)

class TransactionAdmin(admin.ModelAdmin):
    list_display = ('trans_name', 'amount', 'currency', 'trans_type', 'date_trans', 'salon')
    list_filter = ('trans_type', 'salon', 'currency')
    search_fields = ('trans_name', 'salon__name')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(salon__owner=request.user)

    def has_add_permission(self, request):
        return request.user.is_superuser or request.user.owned_salons.exists()

    def has_change_permission(self, request, obj=None):
        if obj is None:
            return True
        return obj.salon.owner == request.user or request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        if obj is None:
            return True
        return obj.salon.owner == request.user or request.user.is_superuser

admin.site.register(Transaction, TransactionAdmin)
