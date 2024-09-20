from rest_framework import serializers
from saloon.models import Salon, Barber, Client, BarberType, Attachment

class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = '__all__'

class SalonSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')

    class Meta:
        model = Salon
        fields = '__all__'

class BarberTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BarberType
        fields = '__all__'

class BarberSerializer(serializers.ModelSerializer):
    user_email = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = Barber
        fields = '__all__'

class ClientSerializer(serializers.ModelSerializer):
    user_email = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = Client
        fields = '__all__'