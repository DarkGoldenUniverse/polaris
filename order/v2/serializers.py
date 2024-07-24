from rest_framework import serializers

from order.models import Order, OrderItem, ORDER_STATUS_MAPPING, ORDER_ITEM_STATUS_MAPPING
from services.serializer import CustomChoiceField


class OrderItemSerializer(serializers.ModelSerializer):
    status = CustomChoiceField(choices=ORDER_ITEM_STATUS_MAPPING, read_only=True)
    total = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = [
            "id",
            "code",
            "name",
            "price",
            "amount",
            "total",
            "comment",
            "status",
            "order",
            "product",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "code", "name", "price", "status", "order", "product", "created_at", "updated_at"]

    @staticmethod
    def get_total(obj) -> str:
        return str(obj.price * obj.amount)


class OrderSerializer(serializers.ModelSerializer):
    status = CustomChoiceField(choices=ORDER_STATUS_MAPPING, read_only=True)
    order_items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ["id", "address", "status", "order_items"]
        read_only_fields = ["id", "status"]
