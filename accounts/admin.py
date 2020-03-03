from django.contrib import admin

from .models import Kasper, Kirsten, Marie, FarMor, TransactionId, KmPrice

class UserAdmin(admin.ModelAdmin):
    list_display = ('id','timestamp', 'category', 'km', 'amount', 'saldo')

class KmAdmin(admin.ModelAdmin):
    list_display = ('price',)


admin.site.register(Kasper, UserAdmin)
admin.site.register(Kirsten, UserAdmin)
admin.site.register(Marie, UserAdmin)
admin.site.register(FarMor, UserAdmin)
admin.site.register(TransactionId)
admin.site.register(KmPrice, KmAdmin)
