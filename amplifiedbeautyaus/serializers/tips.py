from rest_framework import serializers

from amplifiedbeautyaus.models import Tips


class TipsSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    bookmarked = serializers.SerializerMethodField()

    def get_image(self, instance):
        return instance.image.url

    def get_bookmarked(self, instance):
        request = self.context['request']
        try:
            return instance in request.user.customer.bookmarked_tips.all()
        except:
            return False

    class Meta:
        model = Tips
        fields = ('id', 'name', 'image', 'content', 'bookmarked',)
