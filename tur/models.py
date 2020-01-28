from django.db import models
from datetime import date

current_km = 123456

class Ture(models.Model):
    dato = models.DateField(default=date.today)
    km_count = models.IntegerField(default=current_km)
    user_id = models.IntegerField()