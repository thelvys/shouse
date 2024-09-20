from rest_framework import serializers
from salooninventory.models import Item, ItemUsed, ItemPurchase

class ItemSerializer(serializers.ModelSerializer):
    total_value = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    average_purchase_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Item
        fields = '__all__'
        read_only_fields = ('amount_in_default_currency', 'current_stock')

class ItemUsedSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemUsed
        fields = '__all__'

class ItemPurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemPurchase
        fields = '__all__'
        read_only_fields = ('purchase_price_in_default_currency',)