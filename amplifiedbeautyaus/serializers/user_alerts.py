from rest_framework import serializers

from amplifiedbeautyaus.models import UserAlert
from amplifiedbeautyaus.serializers.customer import CustomerSerializer


class UserAlertSerializer(serializers.ModelSerializer):
    user = CustomerSerializer()

    class Meta:
        model = UserAlert
        fields = ('id', 'user', 'text', 'timestamp')
