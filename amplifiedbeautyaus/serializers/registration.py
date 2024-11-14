from rest_framework import serializers


class CustomerRegisterSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=150, write_only=True, required=True)
    last_name = serializers.CharField(max_length=150, write_only=True, required=True)
    email = serializers.EmailField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, max_length=128)
    phone = serializers.CharField(write_only=True, required=True)
