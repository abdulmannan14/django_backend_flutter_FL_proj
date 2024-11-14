from django.contrib.admin import register, ModelAdmin, TabularInline

from amplifiedbeautyaus.models import Customer, CustomerAddresses


class CustomerAddressesInline(TabularInline):
    model = CustomerAddresses


@register(Customer)
class CustomerAdmin(ModelAdmin):
    list_select_related = True
    list_display = ('first_name', 'last_name', 'email')
    inlines = [CustomerAddressesInline]

