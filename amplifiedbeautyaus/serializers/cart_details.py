from rest_framework import serializers

from amplifiedbeautyaus.models import CartDetails
from amplifiedbeautyaus.serializers.product import ProductSerializer


class CartDetailsSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = CartDetails
        fields = ('id', 'cart', 'product', 'quantity', 'sub_total', 'item_notes')
