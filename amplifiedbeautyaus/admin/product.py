from django.contrib.admin import register, ModelAdmin, TabularInline

from amplifiedbeautyaus.models import Product, ProductImages


class ProductImagesInline(TabularInline):
    model = ProductImages


@register(Product)
class ProductAdmin(ModelAdmin):
    list_select_related = True
    list_display = ('name', 'price', 'product_range')
    inlines = [ProductImagesInline]
