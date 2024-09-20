from django.contrib import admin
from .models import Item, ItemUsed, ItemPurchase

class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'currency', 'current_stock', 'salon')
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

admin.site.register(Item, ItemAdmin)

class ItemUsedAdmin(admin.ModelAdmin):
    list_display = ('item', 'shave', 'barber', 'quantity', 'salon')
    list_filter = ('salon',)
    search_fields = ('item__name', 'shave__hairstyle__name', 'barber__user__email', 'salon__name')

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

admin.site.register(ItemUsed, ItemUsedAdmin)

class ItemPurchaseAdmin(admin.ModelAdmin):
    list_display = ('item', 'quantity', 'purchase_price', 'currency', 'purchase_date', 'supplier', 'salon')
    list_filter = ('salon', 'currency', 'purchase_date')
    search_fields = ('item__name', 'supplier', 'salon__name')

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

admin.site.register(ItemPurchase, ItemPurchaseAdmin)
