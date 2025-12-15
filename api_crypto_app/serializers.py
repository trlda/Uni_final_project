from rest_framework import serializers
from .models import CryptoCurrencyPrice

class CryptoPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CryptoCurrencyPrice
        fields = '__all__'