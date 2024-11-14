from rest_framework import serializers

from amplifiedbeautyaus.models import ProductRange
from amplifiedbeautyaus.serializers.product import ProductSerializer


class ProductRangeSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    products = ProductSerializer(many=True)

    def get_image(self, instance):
        return instance.image.url

    class Meta:
        model = ProductRange
        fields = ('id', 'name', 'image', 'color', 'products',)

