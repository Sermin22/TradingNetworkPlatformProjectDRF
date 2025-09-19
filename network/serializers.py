from rest_framework import serializers
from .models import NetworkLink, Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class NetworkLinkSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = NetworkLink
        fields = [
            'id', 'name', 'email', 'country', 'city', 'street', 'house_number', 'network_type',
            'supplier', 'debt_to_supplier', 'created_at', 'level', 'products'
        ]
        read_only_fields = ['debt_to_supplier', 'created_at', 'level']
        # exclude = ("debt_to_supplier",)  # запрет обновления через API