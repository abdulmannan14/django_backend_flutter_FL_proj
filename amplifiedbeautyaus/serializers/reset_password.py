from rest_framework import serializers


class RequestPasswordResetSerializer(serializers.Serializer):
    phone = serializers.CharField(required=False, allow_blank=True, allow_null=True)


class ConfirmPasswordResetSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    code = serializers.CharField(max_length=6)
    password = serializers.CharField(max_length=128)
