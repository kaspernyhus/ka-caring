from django.db import models
from datetime import date


class Tankning(models.Model):
    dato = models.DateField(default=date.today)
    pris = models.FloatField()
    user_id = models.CharField(max_length=50)