from django.contrib import admin

from .models import Ture

class TurAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'km_count', 'user_id', 'extra_pas', 'delta_km', 'price')


admin.site.register(Ture, TurAdmin)