from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers

from account.models import Address


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ["id", "address"]
        read_only_fields = ["id"]


class UserSerializer(serializers.ModelSerializer):
    # address = serializers.PrimaryKeyRelatedField(queryset=Address.objects.all(), many=True)

    class Meta:
        model = get_user_model()
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "username",
            "phone_number",
            "additional_data",
            # "address",
        ]
        read_only_fields = ["id", "email", "username", "additional_data"]


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(label="Username", write_only=True)
    password = serializers.CharField(
        label="Password",
        style={"input_type": "password"},
        trim_whitespace=False,
        write_only=True,
    )

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        if username and password:
            user = authenticate(
                request=self.context.get("request"),
                username=username.lower(),
                password=password,
            )

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication backend.)
            if not user:
                msg = {"password": "Unable to log in with provided credentials."}
                raise serializers.ValidationError(msg, code="authorization")
        else:
            msg = {"password": 'Must include "username" and "password".'}
            raise serializers.ValidationError(msg, code="authorization")

        attrs["user"] = user
        return attrs