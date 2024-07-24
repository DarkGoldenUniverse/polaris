from customer.v2.serializers import CustomerSerializer, AddressSerializer


class AdminAddressSerializer(AddressSerializer):
    pass


class AdminCustomerSerializer(CustomerSerializer):
    addresses = AddressSerializer(many=True, read_only=True)

    class Meta(CustomerSerializer.Meta):
        fields = CustomerSerializer.Meta.fields
        read_only_fields = CustomerSerializer.Meta.read_only_fields
