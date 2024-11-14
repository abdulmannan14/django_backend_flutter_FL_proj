from django.db.models import Sum
from rest_framework import serializers

from amplifiedbeautyaus.models import Cart, CartDetails
from amplifiedbeautyaus.serializers.cart_details import CartDetailsSerializer


class CartSerializer(serializers.ModelSerializer):
    cart_details = CartDetailsSerializer(many=True)
    total = serializers.SerializerMethodField()
    sub_total = serializers.SerializerMethodField()
    delivery_fee = serializers.SerializerMethodField()
    address = serializers.SerializerMethodField()

    def get_address(self, instance):
        if instance.address is not None:
            return instance.address.address
        else:
            return None

    def get_total(self, instance):
        return float(instance.total)

    def get_sub_total(self, instance):
        return float(instance.sub_total)

    def get_delivery_fee(self, instance):
        return float(instance.delivery_fee)

    class Meta:
        model = Cart
        fields = ('id', 'customer', 'cart_details', 'created_at', 'delivery_fee', 'sub_total', 'total', 'address',)


class AddToCartSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    quantity = serializers.IntegerField()
    item_notes = serializers.CharField(max_length=256, allow_blank=True, allow_null=True)
