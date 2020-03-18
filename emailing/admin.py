from django.contrib import admin
from .models import UserPreferences, EmailQue


admin.site.register(UserPreferences)
admin.site.register(EmailQue)