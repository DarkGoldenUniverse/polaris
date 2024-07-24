from rest_framework import serializers

from account.models import User
from customer.v2.admin.serializers import AdminCustomerSerializer
from order.v2.serializers import OrderItemSerializer, OrderSerializer


class AdminOrderItemSerializer(OrderItemSerializer):
    executor = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    creator = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta(OrderItemSerializer.Meta):
        fields = OrderItemSerializer.Meta.fields + ["product_info", "executor", "creator"]
        read_only_fields = OrderItemSerializer.Meta.read_only_fields + ["product_info", "creator"]


class AdminOrderSerializer(OrderSerializer):
    customer = AdminCustomerSerializer()
    order_items = AdminOrderItemSerializer(many=True)
    creator = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta(OrderSerializer.Meta):
        fields = OrderSerializer.Meta.fields + ["customer", "creator"]
        read_only_fields = OrderSerializer.Meta.read_only_fields + ["creator"]
