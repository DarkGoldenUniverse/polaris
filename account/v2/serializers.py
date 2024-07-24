from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "username",
            "additional_data",
        ]
        read_only_fields = ["id", "email", "username"]


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
