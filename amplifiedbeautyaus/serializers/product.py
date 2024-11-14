from django.db.models import Avg
from rest_framework import serializers

from amplifiedbeautyaus.models import Product, ProductReviews, ProductRange, ProductImages
from amplifiedbeautyaus.serializers.customer import CustomerSerializer


class ProductReviewSerializer(serializers.ModelSerializer):
    user = CustomerSerializer()

    class Meta:
        model = ProductReviews
        fields = ('rating', 'review', 'user', 'date_added')


class ProductRangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductRange
        fields = ('id', 'name', 'image', 'color', 'products',)


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImages
        fields = ('id', 'image',)


class ProductSerializer(serializers.ModelSerializer):
    product_images = ProductImageSerializer(many=True)
    reviews = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()
    in_wishlist = serializers.SerializerMethodField()
    product_range = ProductRangeSerializer()

    def get_rating(self, instance):
        try:
            reviews = ProductReviews.objects.filter(product=instance)
            review_average = reviews.aggregate(average=Avg('rating'))
            if reviews.count() < 1:
                return 0.0
            return review_average['average']
        except:
            return 0.0

    def get_reviews(self, instance):
        context = self.context['request']
        serializer = ProductReviewSerializer(
            instance.product_review.all(),
            many=True,
            context={'context': context}
        )
        return serializer.data

    def get_in_wishlist(self, instance):
        request = self.context['request']
        try:
            if request.user.customer:
                return instance in request.user.customer.wishlisted_products.all()
            else:
                return False
        except:
            return False

    class Meta:
        model = Product
        fields = ('id', 'name', 'product_range', 'price', 'description', 'duration', 'fragrance', 'type', 'color',
                  'estimated_timeframe', 'product_images', 'reviews', 'rating', 'in_wishlist',)


class ProductWishlistSerializer(serializers.Serializer):
    id = serializers.IntegerField()
