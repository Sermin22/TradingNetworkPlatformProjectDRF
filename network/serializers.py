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
        # Исключаем из редактирования поля через API, но отображаем при GET-запросах
        read_only_fields = ['debt_to_supplier', 'created_at', 'level']

    def validate(self, data):
        """Валидация бизнес-правил на уровне сериализатора"""

        # Получаем текущий экземпляр (если есть)
        instance = self.instance
        # Безопасно получаем данные. Пробуем взять network_type и supplier из данных запроса,
        # если их нет, пробуем взять их из существующего объекта, если и там нет - вернем None
        network_type = data.get('network_type', getattr(instance, 'network_type', None))
        supplier = data.get('supplier', getattr(instance, 'supplier', None))

        # Правило 1: Завод не может иметь поставщика
        if network_type == 'factory' and supplier is not None:
            raise serializers.ValidationError({
                'supplier': 'Завод не может иметь поставщика'
            })

        # Правило 2: Розничная сеть и ИП должны иметь поставщика
        if network_type in ['retail', 'entrepreneur'] and supplier is None:
            raise serializers.ValidationError({
                'supplier': 'Розничная сеть или ИП должны иметь поставщика'
            })

        # Правило 3: Нельзя ссылаться на самого себя
        if supplier and instance and supplier.id == instance.id:
            raise serializers.ValidationError({
                'supplier': 'Нельзя указывать самого себя в качестве поставщика'
            })

        # Правило 4: Проверка при создании нового объекта
        if not instance and supplier and supplier.id == data.get('id'):
            raise serializers.ValidationError({
                'supplier': 'Нельзя указывать самого себя в качестве поставщика'
            })
        return data
