from django.contrib import admin
from .models import HairstyleTariffHistory, Hairstyle, Shave

class HairstyleTariffHistoryInline(admin.TabularInline):
    model = HairstyleTariffHistory
    extra = 1

class HairstyleAdmin(admin.ModelAdmin):
    list_display = ('name', 'current_tariff', 'currency', 'salon')
    list_filter = ('salon', 'currency')
    search_fields = ('name', 'salon__name')
    inlines = [HairstyleTariffHistoryInline]

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

admin.site.register(Hairstyle, HairstyleAdmin)

class ShaveAdmin(admin.ModelAdmin):
    list_display = ('barber', 'hairstyle', 'amount', 'currency', 'client', 'date_shave', 'status', 'salon')
    list_filter = ('status', 'salon', 'currency')
    search_fields = ('barber__user__email', 'hairstyle__name', 'client__name', 'salon__name')

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

admin.site.register(Shave, ShaveAdmin)
