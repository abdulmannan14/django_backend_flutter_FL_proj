from rest_framework import serializers


class UpdatePaymentSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=128, allow_blank=False, allow_null=False)
