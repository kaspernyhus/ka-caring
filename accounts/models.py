from django.db import models
from datetime import datetime
from django.utils import timezone


class TransactionId(models.Model):
  transaction_id = models.IntegerField(primary_key=True, blank=False, unique=True)
  timestamp = models.DateTimeField(default=timezone.now)
  action = models.CharField(max_length=100)
  user = models.CharField(max_length=20, default='AnonymousUser')
  

class Kirsten(models.Model):
  class Meta:
    verbose_name_plural = '4. Kirsten'

  timestamp = models.DateTimeField(default=timezone.now)
  saldo = models.FloatField(default=0.0)
  amount = models.FloatField(default=0.0)
  km = models.IntegerField(default=0)
  category = models.CharField(blank=True, max_length=50)
  transaction = models.ForeignKey(TransactionId, on_delete=models.CASCADE)


class Marie(models.Model):
  class Meta:
    verbose_name_plural = '1. Marie'

  timestamp = models.DateTimeField(default=timezone.now)
  saldo = models.FloatField(default=0.0)
  amount = models.FloatField(default=0.0)
  km = models.IntegerField(default=0)
  category = models.CharField(blank=True, max_length=50)
  transaction = models.ForeignKey(TransactionId, on_delete=models.CASCADE)


class Kasper(models.Model):
  class Meta:
    verbose_name_plural = '2. Kasper'

  timestamp = models.DateTimeField(default=timezone.now)
  saldo = models.FloatField(default=0.0)
  amount = models.FloatField(default=0.0)
  km = models.IntegerField(default=0)
  category = models.CharField(blank=True, max_length=50)
  transaction = models.ForeignKey(TransactionId, on_delete=models.CASCADE)


class FarMor(models.Model):
  class Meta:
    verbose_name_plural = '3. Farmor & Farfar'

  timestamp = models.DateTimeField(default=timezone.now)
  saldo = models.FloatField(default=0.0)
  amount = models.FloatField(default=0.0)
  km = models.IntegerField(default=0)
  category = models.CharField(blank=True, max_length=50)
  transaction = models.ForeignKey(TransactionId, on_delete=models.CASCADE)


class Guest(models.Model):
  class Meta:
    verbose_name_plural = '5. Guest'

  timestamp = models.DateTimeField(default=timezone.now)
  saldo = models.FloatField(default=0.0)
  amount = models.FloatField(default=0.0)
  km = models.IntegerField(default=0)
  category = models.CharField(blank=True, max_length=50)
  transaction = models.ForeignKey(TransactionId, on_delete=models.CASCADE)


class KmPrice(models.Model):
  class Meta:
    verbose_name_plural = 'Km-Price'

  price = models.FloatField(default=2.0)


class OnBankAccount(models.Model):
  class Meta:
    verbose_name_plural = 'Bank account'

  timestamp = models.DateTimeField(default=timezone.now)
  saldo = models.FloatField(default=0.0)
  category = models.CharField(blank=True, max_length=50, default='')
  user = models.CharField(max_length=20, default='AnonymousUser')
  description = models.CharField(blank=True, default='', max_length=200)
  transaction = models.ForeignKey(TransactionId, on_delete=models.CASCADE, default=1)

  
