from django.contrib import admin
from .models import Salon, Barber, Client

class SalonAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'owner__email')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(owner=request.user)

    def has_add_permission(self, request):
        return True

    def has_change_permission(self, request, obj=None):
        if obj is None:
            return True
        return obj.owner == request.user or request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        if obj is None:
            return True
        return obj.owner == request.user or request.user.is_superuser

admin.site.register(Salon, SalonAdmin)

class BarberAdmin(admin.ModelAdmin):
    list_display = ('user', 'salon', 'barber_type', 'is_active')
    list_filter = ('salon', 'is_active')
    search_fields = ('user__email', 'salon__name')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(salon__owner=request.user)

    def has_add_permission(self, request):
        return Salon.objects.filter(owner=request.user).exists() or request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        if obj is None:
            return True
        return obj.salon.owner == request.user or request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        if obj is None:
            return True
        return obj.salon.owner == request.user or request.user.is_superuser

admin.site.register(Barber, BarberAdmin)

class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'salon', 'phone')
    list_filter = ('salon',)
    search_fields = ('name', 'salon__name')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(salon__owner=request.user)

    def has_add_permission(self, request):
        return Salon.objects.filter(owner=request.user).exists() or request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        if obj is None:
            return True
        return obj.salon.owner == request.user or request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        if obj is None:
            return True
        return obj.salon.owner == request.user or request.user.is_superuser

admin.site.register(Client, ClientAdmin)
