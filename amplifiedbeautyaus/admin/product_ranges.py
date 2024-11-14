from django.contrib.admin import ModelAdmin, register

from amplifiedbeautyaus.models import ProductRange


@register(ProductRange)
class ProductRangeAdmin(ModelAdmin):
    list_select_related = True
    list_display = ('id', 'name',)
