from django.db import models
from datetime import date
from accounts.models import TransactionId


class Ture(models.Model):
  class Meta:
    verbose_name_plural = 'Ture'
    
  date = models.DateField(default=date.today)
  km_count = models.IntegerField(default=0)
  user_id = models.CharField(max_length=50, default=' ')
  extra_pas = models.CharField(blank=True, max_length=50)
  delta_km = models.IntegerField(default=0)
  price = models.FloatField(default=0.0)
  transaction = models.ForeignKey(TransactionId, on_delete=models.CASCADE)
