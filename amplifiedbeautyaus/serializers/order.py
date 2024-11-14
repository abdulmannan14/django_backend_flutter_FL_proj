import geocoder
import googlemaps as googlemaps
from django.conf import settings
from rest_framework import serializers

from amplifiedbeautyaus.models import Order, OrderDetails
from amplifiedbeautyaus.serializers import ProductSerializer

gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)


class OrderDetailsSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    class Meta:
        model = OrderDetails
        fields = ('id', 'product', 'quantity', 'sub_total', 'item_notes',)


class OrderSerializer(serializers.ModelSerializer):
    order_details = OrderDetailsSerializer(many=True)
    status_display = serializers.SerializerMethodField()
    location = serializers.SerializerMethodField()

    def get_location(self, instance):
        # Geocode the Location for this Order
        g = geocoder.google(instance.address.address,
                            key=settings.GOOGLE_MAPS_API_KEY)
        print(g.latlng)
        loc_data = {
            "latitude": g.latlng[0],
            "longitude": g.latlng[1],
        }
        return loc_data

    def get_status_display(self, instance):
        return instance.get_status_display()

    class Meta:
        model = Order
        fields = ('id', 'customer', 'address', 'sub_total', 'status', 'status_display', 'delivery_fee', 'total',
                  'created_at', 'order_details', 'location',)
