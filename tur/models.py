from django.db import models
from datetime import date

class Ture(models.Model):
    dato = models.DateField(default=date.today, auto_now=False)
    km = models.IntegerField(blank=True)
    user_id = models.IntegerField(blank=True)