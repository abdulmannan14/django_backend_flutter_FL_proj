from django.contrib.admin import ModelAdmin, register

from amplifiedbeautyaus.models import Tips


@register(Tips)
class TipsAdmin(ModelAdmin):
    list_select_related = True
    list_display = ('id', 'name',)
