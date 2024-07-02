from order.models import Order
from order.v2.serializers import OrderItemSerializer, OrderSerializer


class AdminOrderItemSerializer(OrderItemSerializer):
    pass


class AdminOrderSerializer(OrderSerializer):
    class Meta:
        model = Order
        fields = ["id", "address", "status", "user", "created_by", "items"]
        read_only_fields = ["id", "status", "created_by"]
