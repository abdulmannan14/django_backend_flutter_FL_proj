from django.contrib.admin import register, ModelAdmin

from amplifiedbeautyaus.models import ProductReviews


@register(ProductReviews)
class ProductReviewAdmin(ModelAdmin):
    list_select_related = True
    list_display = ('product', 'rating', 'review', 'user')
