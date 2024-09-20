from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.db.models import Q
from .models import Salon, Barber, Client, BarberType
from .forms import SalonForm, BarberForm, ClientForm, BarberTypeForm

class SalonOwnerMixin(UserPassesTestMixin):
    def test_func(self):
        salon = self.get_object()
        return self.request.user == salon.owner

class HasSalonMixin(UserPassesTestMixin):
    def test_func(self):
        return Salon.objects.filter(owner=self.request.user).exists()

class SalonListView(ListView):
    model = Salon
    template_name = 'saloon/salon_list.html'
    context_object_name = 'salons'
    paginate_by = 10

    def get_queryset(self):
        queryset = Salon.objects.filter(is_active=True)
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(description__icontains=search_query)
            )
        return queryset.order_by('-created_at')

class SalonCreateView(LoginRequiredMixin, CreateView):
    model = Salon
    form_class = SalonForm
    template_name = 'saloon/salon_form.html'
    success_url = reverse_lazy('salon:salon_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        messages.success(self.request, _("Salon created successfully."))
        return super().form_valid(form)

class SalonUpdateView(LoginRequiredMixin, SalonOwnerMixin, UpdateView):
    model = Salon
    form_class = SalonForm
    template_name = 'saloon/salon_form.html'
    success_url = reverse_lazy('salon:salon_list')

    def form_valid(self, form):
        messages.success(self.request, _("Salon updated successfully."))
        return super().form_valid(form)

class SalonDetailView(LoginRequiredMixin, SalonOwnerMixin, DetailView):
    model = Salon
    template_name = 'saloon/salon_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['barbers'] = self.object.barbers.all().select_related('user')[:5]
        context['clients'] = self.object.clients.all().select_related('user')[:5]
        return context

class SalonDeleteView(LoginRequiredMixin, SalonOwnerMixin, DeleteView):
    """
    Handles the deletion of a salon. Ensures that only the owner can delete the salon and provides error handling.
    """
    model = Salon
    template_name = 'saloon/confirm_delete.html'
    success_url = reverse_lazy('accounts:home')

    def delete(self, request, *args, **kwargs):
        if not self.test_func():
            messages.error(self.request, _("You do not have permission to delete this salon."))
            return redirect('salon:salon_list')
        try:
            response = super().delete(request, *args, **kwargs)
            messages.success(self.request, _("Salon deleted successfully."))
            return response
        except Exception as e:
            messages.error(self.request, _("Failed to delete salon."))
            return redirect('salon:salon_detail', pk=self.object.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cancel_url'] = reverse_lazy('salon:salon_detail', kwargs={'pk': self.object.pk})
        return context

class BarberListView(LoginRequiredMixin, HasSalonMixin, ListView):
    model = Barber
    template_name = 'saloon/barber_list.html'
    context_object_name = 'barbers'
    paginate_by = 10

    def test_func(self):
        salon = self.get_salon()
        return self.request.user == salon.owner
    
    def get_salon(self):
        salon_id = self.kwargs.get('salon_id')
        return get_object_or_404(Salon, pk=salon_id)

    def get_queryset(self):
        salon = self.get_salon()
        return BarberType.objects.filter(salon=salon).order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['salon'] = self.get_salon()
        return context

class BarberCreateView(LoginRequiredMixin, HasSalonMixin, CreateView):
    model = Barber
    form_class = BarberForm
    template_name = 'saloon/barber_form.html'

    def get_success_url(self):
        return reverse_lazy('salon:barber_list')

    def form_valid(self, form):
        form.instance.salon = get_object_or_404(Salon, owner=self.request.user)
        messages.success(self.request, _("Barber created successfully."))
        return super().form_valid(form)

class BarberUpdateView(LoginRequiredMixin, HasSalonMixin, UpdateView):
    model = Barber
    form_class = BarberForm
    template_name = 'saloon/barber_form.html'

    def get_success_url(self):
        return reverse_lazy('salon:barber_list')

    def get_queryset(self):
        salon = get_object_or_404(Salon, owner=self.request.user)
        return Barber.objects.filter(salon=salon)

    def form_valid(self, form):
        messages.success(self.request, _("Barber updated successfully."))
        return super().form_valid(form)

class BarberDeleteView(LoginRequiredMixin, HasSalonMixin, DeleteView):
    model = Barber
    template_name = 'saloon/confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('salon:barber_list')

    def get_queryset(self):
        salon = get_object_or_404(Salon, owner=self.request.user)
        return Barber.objects.filter(salon=salon)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, _("Barber deleted successfully."))
        return super().delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cancel_url'] = reverse_lazy('salon:barber_list')
        return context

class ClientListView(LoginRequiredMixin, HasSalonMixin, ListView):
    model = Client
    template_name = 'saloon/client_list.html'
    context_object_name = 'clients'
    paginate_by = 10

    def test_func(self):
        salon = self.get_salon()
        return self.request.user == salon.owner
    
    def get_salon(self):
        salon_id = self.kwargs.get('salon_id')
        return get_object_or_404(Salon, pk=salon_id)

    def get_queryset(self):
        salon = self.get_salon()
        return BarberType.objects.filter(salon=salon).order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['salon'] = self.get_salon()
        return context

class ClientCreateView(LoginRequiredMixin, HasSalonMixin, CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'saloon/client_form.html'

    def get_success_url(self):
        return reverse_lazy('salon:client_list')

    def form_valid(self, form):
        form.instance.salon = get_object_or_404(Salon, owner=self.request.user)
        messages.success(self.request, _("Client created successfully."))
        return super().form_valid(form)

class ClientUpdateView(LoginRequiredMixin, HasSalonMixin, UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'saloon/client_form.html'

    def get_success_url(self):
        return reverse_lazy('salon:client_list')

    def get_queryset(self):
        salon = get_object_or_404(Salon, owner=self.request.user)
        return Client.objects.filter(salon=salon)

    def form_valid(self, form):
        messages.success(self.request, _("Client updated successfully."))
        return super().form_valid(form)

class ClientDeleteView(LoginRequiredMixin, HasSalonMixin, DeleteView):
    model = Client
    template_name = 'saloon/confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('salon:client_list')

    def get_queryset(self):
        salon = get_object_or_404(Salon, owner=self.request.user)
        return Client.objects.filter(salon=salon)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, _("Client deleted successfully."))
        return super().delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cancel_url'] = reverse_lazy('salon:client_list')
        return context

class BarberTypeListView(LoginRequiredMixin, HasSalonMixin, ListView):
    model = BarberType
    template_name = 'saloon/barber_type_list.html'
    context_object_name = 'barber_types'
    paginate_by = 10

    def test_func(self):
        salon = self.get_salon()
        return self.request.user == salon.owner
    
    def get_salon(self):
        salon_id = self.kwargs.get('salon_id')
        return get_object_or_404(Salon, pk=salon_id)

    def get_queryset(self):
        salon = self.get_salon()
        return BarberType.objects.filter(salon=salon).order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['salon'] = self.get_salon()
        return context

class BarberTypeCreateView(LoginRequiredMixin, HasSalonMixin, CreateView):
    model = BarberType
    form_class = BarberTypeForm
    template_name = 'saloon/barber_type_form.html'

    def get_success_url(self):
        return reverse_lazy('salon:barber_type_list')

    def form_valid(self, form):
        form.instance.salon = get_object_or_404(Salon, owner=self.request.user)
        messages.success(self.request, _("Barber Type created successfully."))
        return super().form_valid(form)

class BarberTypeUpdateView(LoginRequiredMixin, HasSalonMixin, UpdateView):
    model = BarberType
    form_class = BarberTypeForm
    template_name = 'saloon/barber_type_form.html'

    def get_success_url(self):
        return reverse_lazy('salon:barber_type_list')

    def get_queryset(self):
        salon = get_object_or_404(Salon, owner=self.request.user)
        return BarberType.objects.filter(salon=salon)

    def form_valid(self, form):
        messages.success(self.request, _("Barber Type updated successfully."))
        return super().form_valid(form)
    
    def test_func(self):
        barber_type = self.get_object()
        return self.request.user == barber_type.salon.owner
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['salon'] = self.object.salon
        return context

class BarberTypeDeleteView(LoginRequiredMixin, HasSalonMixin, DeleteView):
    model = BarberType
    template_name = 'saloon/confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('salon:barber_type_list')

    def get_queryset(self):
        salon = get_object_or_404(Salon, owner=self.request.user)
        return BarberType.objects.filter(salon=salon)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, _("Barber Type deleted successfully."))
        return super().delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cancel_url'] = reverse_lazy('salon:barber_type_list')
        return context