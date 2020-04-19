from django.contrib import admin

from .models import Tankning, Betaling, Udgift

class TankningAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'amount', 'user_id')

class BetalingAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'amount', 'user_id', 'description')

class UdgiftAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'amount', 'description', 'user_id')


admin.site.register(Tankning, TankningAdmin)
admin.site.register(Betaling, BetalingAdmin)
admin.site.register(Udgift, UdgiftAdmin)