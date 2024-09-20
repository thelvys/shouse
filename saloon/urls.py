from django.urls import path
from . import views

app_name = 'salon'

urlpatterns = [
    # Salon URLs
    path('', views.SalonListView.as_view(), name='salon_list'),
    path('create/', views.SalonCreateView.as_view(), name='salon_create'),
    path('<int:pk>/', views.SalonDetailView.as_view(), name='salon_detail'),
    path('<int:pk>/update/', views.SalonUpdateView.as_view(), name='salon_update'),
    path('<int:pk>/delete/', views.SalonDeleteView.as_view(), name='salon_delete'),

    # Barber URLs
    path('<int:salon_id>/barbers/', views.BarberListView.as_view(), name='barber_list'),
    path('<int:salon_id>/barbers/create/', views.BarberCreateView.as_view(), name='barber_create'),
    path('<int:salon_id>/barbers/<int:pk>/update/', views.BarberUpdateView.as_view(), name='barber_update'),
    path('<int:salon_id>/barbers/<int:pk>/delete/', views.BarberDeleteView.as_view(), name='barber_delete'),

    # Client URLs
    path('<int:salon_id>/clients/', views.ClientListView.as_view(), name='client_list'),
    path('<int:salon_id>/clients/create/', views.ClientCreateView.as_view(), name='client_create'),
    path('<int:salon_id>/clients/<int:pk>/update/', views.ClientUpdateView.as_view(), name='client_update'),
    path('<int:salon_id>/clients/<int:pk>/delete/', views.ClientDeleteView.as_view(), name='client_delete'),

    # BarberType URLs
    path('<int:salon_id>/barber-types/', views.BarberTypeListView.as_view(), name='barber_type_list'),
    path('<int:salon_id>/barber-types/create/', views.BarberTypeCreateView.as_view(), name='barber_type_create'),
    path('<int:salon_id>/barber-types/<int:pk>/update/', views.BarberTypeUpdateView.as_view(), name='barber_type_update'),
    path('<int:salon_id>/barber-types/<int:pk>/delete/', views.BarberTypeDeleteView.as_view(), name='barber_type_delete'),
]