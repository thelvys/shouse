from rest_framework import serializers
from saloonservices.models import HairstyleTariffHistory, Hairstyle, Shave

class HairstyleTariffHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = HairstyleTariffHistory
        fields = '__all__'

class HairstyleSerializer(serializers.ModelSerializer):
    tariff_history = HairstyleTariffHistorySerializer(many=True, read_only=True)

    class Meta:
        model = Hairstyle
        fields = '__all__'

class ShaveSerializer(serializers.ModelSerializer):
    total_amount = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    tariff_difference = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Shave
        fields = '__all__'
        read_only_fields = ('amount_in_default_currency',)