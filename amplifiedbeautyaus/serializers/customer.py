from rest_framework import serializers

from amplifiedbeautyaus.models import Customer, CustomerAddresses


class CustomerSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    def get_image(self, instance):
        return instance.avatar.url

    class Meta:
        model = Customer
        fields = ('first_name', 'last_name', 'email', 'image')


class CustomerAddressSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()

    class Meta:
        model = CustomerAddresses
        fields = ('id', 'customer', 'address', 'default',)


class CustomerSetAddressSerializer(serializers.Serializer):
    address = serializers.CharField(max_length=512)


class CustomerCreateAddressSerializer(serializers.Serializer):
    address = serializers.CharField(max_length=512)