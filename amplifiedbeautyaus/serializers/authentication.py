from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=64)
    password = serializers.CharField(max_length=48)


class AppleLoginSerializer(serializers.Serializer):
    access_token = serializers.CharField(max_length=1024, required=True, trim_whitespace=True)
