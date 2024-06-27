from rest_framework import serializers

from inventory.models import Category, Inventory, UNIT_MAPPING
from services.serializer import CustomChoiceField


class CategorySerializer(serializers.ModelSerializer):
    parent = serializers.StringRelatedField()

    class Meta:
        model = Category
        fields = ["id", "name", "parent", "path"]
        read_only_fields = fields


class InventorySerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    remaining_amount = serializers.SerializerMethodField()
    unit = CustomChoiceField(choices=UNIT_MAPPING)

    class Meta:
        model = Inventory
        fields = [
            "id",
            "code",
            "name",
            "price",
            "max_price",
            "amount",
            "executed_amount",
            "remaining_amount",
            "unit",
            "note",
            "image_url",
            "description",
            "category",
        ]
        read_only_fields = fields

    @staticmethod
    def get_remaining_amount(obj) -> str:
        return str(obj.amount - obj.executed_amount)
