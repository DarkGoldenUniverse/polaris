from rest_framework import serializers

from customer.models import Address, Customer


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ["id", "address"]
        read_only_fields = ["id"]


class CustomerSerializer(serializers.ModelSerializer):
    addresses = AddressSerializer(many=True)

    class Meta:
        model = Customer
        fields = ["id", "name", "phone_number", "additional_data", "addresses"]
        read_only_fields = ["id", "addresses"]
