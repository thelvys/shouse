from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HairstyleViewSet, HairstyleTariffHistoryViewSet, ShaveViewSet

router = DefaultRouter()
router.register(r'hairstyles', HairstyleViewSet, basename='hairstyle')
router.register(r'hairstyle-tariff-history', HairstyleTariffHistoryViewSet, basename='hairstyletariffhistory')
router.register(r'shaves', ShaveViewSet, basename='shave')

urlpatterns = [
    path('', include(router.urls)),
]