from rest_framework import serializers

from inventory.models import UNIT_MAPPING
from order.models import Order, OrderItem
from services.serializer import CustomChoiceField


class OrderSerializer(serializers.ModelSerializer):
    parent = serializers.StringRelatedField()

    class Meta:
        model = Order
        fields = ["id", "address", "status", "user", "created_by"]
        read_only_fields = ["id", "created_by"]


class OrderItemSerializer(serializers.ModelSerializer):
    unit = CustomChoiceField(choices=UNIT_MAPPING)

    class Meta:
        model = OrderItem
        fields = [
            "id",
            "code",
            "name",
            "price",
            "amount",
            "unit",
            "comment",
            "status",
            "order",
            "product",
            "assign_to",
            "created_by",
        ]
        read_only_fields = ["id", "code", "name", "price", "unit", "created_by"]
