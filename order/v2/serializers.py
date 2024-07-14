from rest_framework import serializers

from inventory.models import UNIT_MAPPING
from order.models import Order, OrderItem, ORDER_STATUS_MAPPING, ORDER_ITEM_STATUS_MAPPING
from services.serializer import CustomChoiceField


class OrderItemSerializer(serializers.ModelSerializer):
    unit = CustomChoiceField(choices=UNIT_MAPPING, read_only=True)
    status = CustomChoiceField(choices=ORDER_ITEM_STATUS_MAPPING, read_only=True)

    class Meta:
        model = OrderItem
        fields = ["id", "code", "name", "price", "amount", "unit", "comment", "status", "order", "product"]
        read_only_fields = ["id", "code", "name", "price", "unit", "status", "order", "product"]

    @classmethod
    def add_fields(cls, new_fields, new_read_only_fields):
        """
        Dynamically add fields and read_only_fields.
        new_fields should be a list of field names to add to the fields list.
        new_read_only_fields should be a list of field names to add to the read_only_fields list.
        """
        cls.Meta.fields += new_fields
        cls.Meta.read_only_fields += new_read_only_fields


class OrderSerializer(serializers.ModelSerializer):
    status = CustomChoiceField(choices=ORDER_STATUS_MAPPING, read_only=True)
    order_items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ["id", "address", "status", "order_items"]
        read_only_fields = ["id", "address", "status", "order_items"]

    @classmethod
    def add_fields(cls, new_fields, new_read_only_fields):
        """
        Dynamically add fields and read_only_fields.
        new_fields should be a list of field names to add to the fields list.
        new_read_only_fields should be a list of field names to add to the read_only_fields list.
        """
        cls.Meta.fields += new_fields
        cls.Meta.read_only_fields += new_read_only_fields
