from django.contrib.admin import ModelAdmin, register

from amplifiedbeautyaus.models import Cart


@register(Cart)
class CartAdmin(ModelAdmin):
    list_select_related = True
    list_display = ('id', 'customer', 'total', 'created_at')
