from django.contrib.admin import ModelAdmin, register

from amplifiedbeautyaus.models import CartDetails


@register(CartDetails)
class CartDetailsAdmin(ModelAdmin):
    list_select_related = True
    list_display = ('id', 'product', 'quantity', 'sub_total', 'item_notes')
