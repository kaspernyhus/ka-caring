from django.db import models
from datetime import datetime
from django.utils import timezone


class TransactionId(models.Model):
    transaction_id = models.IntegerField(primary_key=True, blank=False, unique=True)
    timestamp = models.DateTimeField(default=timezone.now)
    action = models.CharField(max_length=100)
    user = models.CharField(max_length=20, default='AnonymousUser')
    

class Kirsten(models.Model):
    timestamp = models.DateTimeField(default=timezone.now)
    saldo = models.FloatField(default=0.0)
    amount = models.FloatField(default=0.0)
    km = models.IntegerField(default=0)
    category = models.CharField(blank=True, max_length=50)
    transaction = models.ForeignKey(TransactionId, on_delete=models.CASCADE)


class Marie(models.Model):
    timestamp = models.DateTimeField(default=timezone.now)
    saldo = models.FloatField(default=0.0)
    amount = models.FloatField(default=0.0)
    km = models.IntegerField(default=0)
    category = models.CharField(blank=True, max_length=50)
    transaction = models.ForeignKey(TransactionId, on_delete=models.CASCADE)


class Kasper(models.Model):
    timestamp = models.DateTimeField(default=timezone.now)
    saldo = models.FloatField(default=0.0)
    amount = models.FloatField(default=0.0)
    km = models.IntegerField(default=0)
    category = models.CharField(blank=True, max_length=50)
    transaction = models.ForeignKey(TransactionId, on_delete=models.CASCADE)


class FarMor(models.Model):
    timestamp = models.DateTimeField(default=timezone.now)
    saldo = models.FloatField(default=0.0)
    amount = models.FloatField(default=0.0)
    km = models.IntegerField(default=0)
    category = models.CharField(blank=True, max_length=50)
    transaction = models.ForeignKey(TransactionId, on_delete=models.CASCADE)

class KmPrice(models.Model):
    price = models.FloatField(default=2.0)


class OnBankAccount(models.Model):
    timestamp = models.DateTimeField(default=timezone.now)
    saldo = models.FloatField(default=0.0)
    category = models.CharField(blank=True, max_length=50, default='')
    description = models.CharField(blank=True, max_length=200, default='')
    transaction = models.ForeignKey(TransactionId, on_delete=models.CASCADE, default=1)

  
