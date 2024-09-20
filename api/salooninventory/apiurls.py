from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ItemViewSet, ItemUsedViewSet, ItemPurchaseViewSet

router = DefaultRouter()
router.register(r'items', ItemViewSet, basename='item')
router.register(r'items-used', ItemUsedViewSet, basename='itemused')
router.register(r'item-purchases', ItemPurchaseViewSet, basename='itempurchase')

urlpatterns = [
    path('', include(router.urls)),
]