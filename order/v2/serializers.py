from rest_framework import serializers

from inventory.models import UNIT_MAPPING
from order.models import Order, OrderItem, ORDER_STATUS_MAPPING, ORDER_ITEM_STATUS_MAPPING
from services.serializer import CustomChoiceField


class OrderItemSerializer(serializers.ModelSerializer):
    assign_to = serializers.StringRelatedField()
    created_by = serializers.StringRelatedField()
    unit = CustomChoiceField(choices=UNIT_MAPPING)
    status = CustomChoiceField(choices=ORDER_ITEM_STATUS_MAPPING)

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


class OrderSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField()
    status = CustomChoiceField(choices=ORDER_STATUS_MAPPING)
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ["id", "address", "status", "user", "created_by", "items"]
        read_only_fields = ["id", "created_by"]
