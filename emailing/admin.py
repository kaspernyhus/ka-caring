from django.contrib import admin
from .models import EmailPreferences, EmailQue


class EmailPrefAdmin(admin.ModelAdmin):
    list_display = ('user_id','monthly_saldo', 'udgift_oprettet', 'tankning_oprettet', 'tur_oprettet')

admin.site.register(EmailPreferences, EmailPrefAdmin)
admin.site.register(EmailQue)