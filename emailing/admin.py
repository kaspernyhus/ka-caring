from django.contrib import admin
from .models import UserPreferences, EmailQue


class EmailPrefAdmin(admin.ModelAdmin):
    list_display = ('id','monthly_saldo', 'udgift_oprettet', 'tankning_oprettet', 'tur_oprettet')

admin.site.register(UserPreferences, EmailPrefAdmin)
admin.site.register(EmailQue)