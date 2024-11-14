from django.contrib import admin

from amplifiedbeautyaus.models import PasswordResetCode


@admin.register(PasswordResetCode)
class PasswordResetAdmin(admin.ModelAdmin):
    list_select_related = True
    list_display = ('user', 'code', 'created', 'used',)
