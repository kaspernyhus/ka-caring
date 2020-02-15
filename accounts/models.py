from django.db import models
from datetime import datetime
from django.utils import timezone


class TransactionId(models.Model):
    transaction_id = models.IntegerField(primary_key=True, blank=False, unique=True)
    timestamp = models.DateTimeField(default=timezone.now)
    action = models.CharField(max_length=100)
    user = models.CharField(max_length=20, default='Ukendt')
    

class Kirsten(models.Model):
    timestamp = models.DateTimeField(auto_now=True)
    saldo = models.FloatField()
    amount = models.FloatField(default=0.0)
    km = models.IntegerField()
    category = models.CharField(blank=True, max_length=50)
    transaction = models.ForeignKey(TransactionId, on_delete=models.CASCADE)


class Marie(models.Model):
    timestamp = models.DateTimeField(auto_now=True)
    saldo = models.FloatField()
    amount = models.FloatField(default=0.0)
    km = models.IntegerField()
    category = models.CharField(blank=True, max_length=50)
    transaction = models.ForeignKey(TransactionId, on_delete=models.CASCADE)


class Kasper(models.Model):
    timestamp = models.DateTimeField(auto_now=True)
    saldo = models.FloatField()
    amount = models.FloatField(default=0.0)
    km = models.IntegerField()
    category = models.CharField(blank=True, max_length=50)
    transaction = models.ForeignKey(TransactionId, on_delete=models.CASCADE)


class FarMor(models.Model):
    timestamp = models.DateTimeField(auto_now=True)
    saldo = models.FloatField()
    amount = models.FloatField(default=0.0)
    km = models.IntegerField()
    category = models.CharField(blank=True, max_length=50)
    transaction = models.ForeignKey(TransactionId, on_delete=models.CASCADE)