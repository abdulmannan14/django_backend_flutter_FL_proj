from django.contrib.admin import ModelAdmin, register

from amplifiedbeautyaus.models import UserAlert


@register(UserAlert)
class UserAlertAdmin(ModelAdmin):
    list_select_related = True
    list_display = ('id', 'text', 'timestamp',)
