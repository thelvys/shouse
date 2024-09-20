from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SalonViewSet, BarberViewSet, ClientViewSet, BarberTypeViewSet, AttachmentViewSet

router = DefaultRouter()
router.register(r'salons', SalonViewSet, basename='salon')
router.register(r'barber-types', BarberTypeViewSet, basename='barbertype')
router.register(r'barbers', BarberViewSet, basename='barber')
router.register(r'clients', ClientViewSet, basename='client')
router.register(r'attachments', AttachmentViewSet, basename='attachment')

urlpatterns = [
    path('', include(router.urls)),
]