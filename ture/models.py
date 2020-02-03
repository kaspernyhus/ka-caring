from django.db import models
from datetime import date
from accounts.models import TransactionId


class Ture(models.Model):
    date = models.DateField(default=date.today)
    km_count = models.IntegerField()
    user_id = models.CharField(max_length=50)
    extra_pas = models.CharField(blank=True, max_length=50)
    delta_km = models.IntegerField()
    price = models.FloatField()
    transaction = models.ForeignKey(TransactionId, on_delete=models.CASCADE)
