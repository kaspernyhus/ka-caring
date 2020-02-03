from django.db import models
from datetime import date
from accounts.models import TransactionId


class Tankning(models.Model):
    date = models.DateField(default=date.today)
    amount = models.FloatField()
    user_id = models.CharField(max_length=50)
    transaction = models.ForeignKey(TransactionId, on_delete=models.CASCADE)


class Betaling(models.Model):
    date = models.DateField(default=date.today)
    amount = models.FloatField()
    user_id = models.CharField(max_length=50)
    transaction = models.ForeignKey(TransactionId, on_delete=models.CASCADE)


class Udgift(models.Model):
    date = models.DateField(default=date.today)
    amount = models.FloatField()
    description = models.CharField(max_length=200)
    user_id = models.CharField(max_length=50)
    transaction = models.ForeignKey(TransactionId, on_delete=models.CASCADE)