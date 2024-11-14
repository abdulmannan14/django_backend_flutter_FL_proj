from django.contrib.admin import register, ModelAdmin, TabularInline

from amplifiedbeautyaus.models import Order, OrderDetails


class OrderDetailsInline(TabularInline):
    model = OrderDetails


@register(Order)
class OrderAdmin(ModelAdmin):
    list_select_related = True
    list_display = ('id', 'customer', 'address', 'total', 'created_at')
    inlines = [OrderDetailsInline]
