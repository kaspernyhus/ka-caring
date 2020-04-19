from django.db import models
from datetime import date
from accounts.models import TransactionId


class Tankning(models.Model):
  class Meta:
    verbose_name_plural = 'Tankninger'

  date = models.DateField(default=date.today)
  amount = models.FloatField()
  user_id = models.CharField(max_length=50)
  transaction = models.ForeignKey(TransactionId, on_delete=models.CASCADE)


class Betaling(models.Model):
  class Meta:
    verbose_name_plural = 'Betalinger'

  date = models.DateField(default=date.today)
  amount = models.FloatField()
  user_id = models.CharField(max_length=50)
  transaction = models.ForeignKey(TransactionId, on_delete=models.CASCADE)
  is_indskud = models.BooleanField(blank=True)
  description = models.CharField(default=None, max_length=200, blank=True, null=True)


class Udgift(models.Model):
  class Meta:
    verbose_name_plural = 'Udgifter'

  date = models.DateField(default=date.today)
  amount = models.FloatField()
  description = models.CharField(max_length=200)
  user_id = models.CharField(max_length=50)
  transaction = models.ForeignKey(TransactionId, on_delete=models.CASCADE)