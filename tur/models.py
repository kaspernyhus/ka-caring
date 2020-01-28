from django.db import models
from datetime import date


class Ture(models.Model):
    dato = models.DateField(default=date.today)
    km_count = models.IntegerField()
    user_id = models.CharField(max_length=50)
    extra_pas = models.CharField(blank=True, max_length=50)